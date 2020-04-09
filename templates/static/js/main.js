let col = [];

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
    document.getElementById("folder-structure").style.display = "none";
    clearCol(0);
}

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
    clearCol(0);
}


function onBallGenerationDone(dataDict) {
    document.getElementById("folder-structure").style.display = "block";
    buildFolders(dataDict);
    const plotly_data = JSON.parse(dataDict.plotly_json);
    let layout = plotly_data.layout;
    layout.dragmode = 'pan';
    Plotly.newPlot('ballPlot', plotly_data.data, layout, {scrollZoom: true});

    buildFullTree(dataDict.plotly_full_tree);

}

function buildFullTree(plotly_full_tree) {
    let plotly_data = JSON.parse(plotly_full_tree);
    // let plotly_data = plotly_full_tree;
    let layout = plotly_data.layout;
    Plotly.newPlot('fullTree', plotly_data.data, layout, {staticPlot: true});
}

window.onload = function () {
    col = [document.getElementById("col1"), document.getElementById("col2"),
        document.getElementById("col3")];
    let submitForm = document.getElementById("input-words");
    submitForm.addEventListener('submit', requestBallGeneration);
    // document.getElementById("input-file").addEventListener("submit", requestBallGeneration);
    document.getElementById("upload-button").addEventListener("click", requestBallGenerationFromFile);

};