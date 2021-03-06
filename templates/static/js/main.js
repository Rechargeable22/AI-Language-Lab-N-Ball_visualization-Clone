let col = [];
let frame = 0;
let frame_data = null;
let log_data = null;

/**
 * >>>>>>>>>>>>>
 * Functions used by the buildFolders function
 */
const clearCol = (colNum) => {
    console.assert(colNum >= 0 && colNum < 3, "False index: " + colNum);
    let child = col[colNum].lastElementChild;
    while (child) {
        col[colNum].removeChild(child);
        child = col[colNum].lastElementChild;
    }
    if (colNum > 0) {
        for (var c = col[colNum - 1].firstChild; c !== null; c = c.nextSibling) {
            c.classList.remove("active")
        }
    }
    if (colNum < 2) {
        clearCol(colNum + 1); // clear subsequent columns
    }
};


function createTextDiv(t) {
    const divNode = document.createElement("a");
    const text = document.createTextNode(t);
    divNode.className = "list-group-item list-group-item-action";
    divNode.appendChild(text);
    divNode.classList.add("clickable");
    return divNode;
}

function createThirdColumnDiv(t) {
    const divElement = document.createElement("div");

    divElement.className = "list-group-item list-group-item-action";

    // textNode.classList.add("clickable");

    const textElement = document.createElement("p");
    const text = document.createTextNode(t);
    textElement.appendChild(text);
    divElement.appendChild(textElement);

    const figureElement = document.createElement("div");
    figureElement.class = "container";
    figureElement.id = "word-path-figure";
    divElement.appendChild(figureElement);

    return divElement;
}

/**
 * Renders an interactive folder structure explaining the different meanings of words.
 * @param dataDict: Object containing the information needed to generate the folders.
 */
function buildFolders(dataDict) {
    let col1 = col[0];
    let col2 = col[1];
    let col3 = col[2];

    for (const key in dataDict.input_words) {
        const word = dataDict.input_words[key]
        const divNode = createTextDiv(dataDict.input_words[key]);
        divNode.addEventListener("click", function () {
            clearCol(1);
            divNode.classList.add("active");

            const elementsToAdd = dataDict.word_senses[dataDict.input_words[key]];

            for (const [index_word_sense, element] of elementsToAdd.entries()) {
                const textElement = createTextDiv(element);
                textElement.addEventListener("click", function () {
                    clearCol(2);
                    textElement.classList.add("active");
                    const definition = createThirdColumnDiv(dataDict.word_definitions[word][index_word_sense]);
                    col3.appendChild(definition);

                    let plotly_data = JSON.parse(dataDict.word_path_fig[word][index_word_sense]);
                    let layout = plotly_data.layout;
                    plotly_data.data[0].marker.color = plotly_data.data[0].marker.color.map(({color}) => "#611111");
                    Plotly.newPlot('word-path-figure', plotly_data.data, layout, {staticPlot: true});

                    setInterval(function () {
                        var randomColor = "#000000".replace(/0/g, function () {
                            return (~~(Math.random() * 16)).toString(16);
                        });
                        let update = {
                            "marker.color": randomColor,
                        };
                        Plotly.restyle('word-path-figure', update)
                    }, 200);
                });
                col2.appendChild(textElement)
            }
        });
        col1.appendChild(divNode);
    }
}

/**
 * Renders the position in the task queue to the website.
 * @param data: object containing the position and type of queue the task is in
 */
function displayQueuePosition(data) {
    const queuedJobIds = data.queued_job_ids;
    const jobPosition = parseInt(queuedJobIds.indexOf(data.task_id));
    const priority = data.queue_priority;

    if (jobPosition === -1) {
        document.getElementById('waiting-queue').style.display = "none";
        document.getElementById('generating-ball').style.display = "flex";

    } else {
        document.getElementById('waiting-queue').style.display = "flex";
        const text = "Server is busy generating balls. " +
            "Waiting in " + priority + " priority queue at position " + (jobPosition + 1) + " of " + queuedJobIds.length + ".";
        document.getElementById("queue-text").textContent = text;
    }
}

/**
 * Client side function that calls the server and requests an update on the ball generation task once every second
 * (active polling).
 * Propagates the current position in the task queue.
 * Calls functions to render received data on success.
 * @param data
 */
function requestBallGenerationStatus(data) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/tasks', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onload = function () {
        const res = JSON.parse(this.responseText);
        if (res.status == 'failed') {
            return false;
        }

        displayQueuePosition(res.data);
        if (res.data.task_status === 'finished') {
            document.getElementById('generating-ball').style.display = "none";
            onBallGenerationDone(JSON.parse(res.data.task_result));
            return false;
        }
        if (res.data.task_status === 'failed') {
            return false;
        }
        setTimeout(function () {
            requestBallGenerationStatus(res.data);  // Active Polling
        }, 1000);
    };

    xhr.send(JSON.stringify(data));
}

/**
 * Requests the server to start the ball generation process for a file uploaded by the user.
 */
function requestBallGenerationFromFile() {
    let formData = new FormData();
    const file = document.getElementById('fileval').files[0];
    formData.append('file', file);

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/file', true);

    xhr.onload = function () {
        const response = JSON.parse(this.responseText);
        requestBallGenerationStatus(response.data);
    };

    xhr.send(formData);
}

/**
 * Requests the server to start the ball generation process from user input.
 */
function requestBallGeneration(e) {
    e.preventDefault();

    let inputWords = document.getElementById('input-text-field').value;
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    xhr.onload = function () {
        const response = JSON.parse(this.responseText);
        requestBallGenerationStatus(response.data);
    };

    xhr.send("inputWords=" + inputWords);
}

/**
 * Renders received data from finished ball generation on the website.
 * @param dataDict: Object containing data to render the plotly plots and the generation animation.
 */
function onBallGenerationDone(dataDict) {
    frame = 0;
    // document.getElementById("folder-structure").style.display = "block";
    document.getElementById("generationOut").style.display = "block";
    // buildFolders(dataDict);  // not anymore :(
    if (dataDict.plotly_json) {
        const plotly_data = JSON.parse(dataDict.plotly_json);
        let layout = plotly_data.layout;
        layout.dragmode = 'pan';
        Plotly.newPlot('ballPlot', plotly_data.data, layout, {scrollZoom: true});
        buildFullTree(dataDict.plotly_full_tree);
        document.getElementById("ballPlotContainer").style.display="block";
        document.getElementById("fullTreeContainer").style.display="block";
    } else {
        // close useless plots
        document.getElementById("ballPlotContainer").style.display="none";
        document.getElementById("fullTreeContainer").style.display="none";
    }
    frame_data = dataDict.plotly_animation;
    log_data = dataDict.generation_log;
    drawDebug()

}

/**
 * Renders ball generation
 */
function drawDebug() {
    const animation_data = JSON.parse(frame_data[frame]);
    layout = animation_data.layout;
    layout.dragmode = 'pan';
    Plotly.newPlot('animationPlot', animation_data.data, layout, {scrollZoom: true});
    document.getElementById("logText").textContent = log_data[frame];
    document.getElementById("animationPlotContainer").style.display="block";

}

/**
 * Renders a family tree of the generated balls showcasing the parent child relationships.
 * @param plotly_full_tree: JSON encoded plotly object that represents the tree.
 */
function buildFullTree(plotly_full_tree) {
    let plotly_data = JSON.parse(plotly_full_tree);
    let layout = plotly_data.layout;
    Plotly.newPlot('fullTree', plotly_data.data, layout, {staticPlot: true});
}

/**
 * Takes a step forward in the ball generation animation.
 */
function debugNextStep() {
    if (frame_data && frame + 1 < frame_data.length)
        frame += 1;
    drawDebug()
}

/**
 * Takes a step forward in the ball generation animation.
 */
function debugPreviousStep() {
    if (frame_data && frame > 0)
        frame -= 1;
    drawDebug()
}

window.onload = function () {

    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal
    btn.onclick = function() {
      modal.style.display = "block";
    };

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    };

    col = [document.getElementById("col1"), document.getElementById("col2"),
        document.getElementById("col3")];
    let submitForm = document.getElementById("input-words");
    submitForm.addEventListener('submit', requestBallGeneration);
    // document.getElementById("input-file").addEventListener("submit", requestBallGeneration);
    document.getElementById("upload-button").addEventListener("click", requestBallGenerationFromFile);
    document.getElementById("previous-step-button").addEventListener("click", debugPreviousStep);
    document.getElementById("next-step-button").addEventListener("click", debugNextStep);

};