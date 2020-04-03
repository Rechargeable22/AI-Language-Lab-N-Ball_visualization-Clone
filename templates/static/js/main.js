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

function buildFolders(dataDict) {
    let col1 = col[0];
    let col2 = col[1];
    let col3 = col[2];

    for (const key in dataDict.input_words) {
        const divNode = createTextDiv(dataDict.input_words[key]);
        divNode.addEventListener("click", function () {
            clearCol(1);
            divNode.classList.add("active");

            const elementsToAdd = dataDict.word_senses[dataDict.input_words[key]];

            for (const [index, element] of elementsToAdd.entries()) {
                const textElement = createTextDiv(element);
                textElement.addEventListener("click", function () {
                    clearCol(2);
                    textElement.classList.add("active");
                    const definition = createTextDiv(dataDict.word_definitions[dataDict.input_words[key]][index]);
                    col3.appendChild(definition);
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
    buildFolders(dataDict);
    const plotly_data = JSON.parse(dataDict.plotly_json);
    let layout = plotly_data.layout;
    layout.dragmode = 'pan';
    Plotly.newPlot('ballPlot', plotly_data.data, layout, {scrollZoom: true});
}

window.onload = function () {
    col = [document.getElementById("col1"), document.getElementById("col2"),
        document.getElementById("col3")];
    let submitForm = document.getElementById("input-words");
    submitForm.addEventListener('submit', requestBallGeneration);
    // document.getElementById("input-file").addEventListener("submit", requestBallGeneration);
    document.getElementById("upload-button").addEventListener("click", requestBallGenerationFromFile);

};