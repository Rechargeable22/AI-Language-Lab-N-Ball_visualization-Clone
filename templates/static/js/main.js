col1 = document.getElementById("col1");
col2 = document.getElementById("col2");
col3 = document.getElementById("col3");


let dataDict = {
    ["ThemaA"]: ["A1", "A2", "A3", "A4","A5", "A6", "A7", "A8"],
    ["ThemaB"]: ["B1", "B2", "B3", "B4"],
    ["ThemaC"]: ["C1", "C2", "C3", "C4"]
};

function clearSecondCol() {
    let child = col2.lastElementChild;
    while (child) {
        col2.removeChild(child);
        child = col2.lastElementChild;
    }
    for(var c=col1.firstChild; c!==null; c=c.nextSibling) {
      c.classList.remove("active")
    }
}

function clearThirdCol() {
    let child = col3.lastElementChild;
    while (child) {
        col3.removeChild(child);
        child = col3.lastElementChild;
    }
      for(var c=col2.firstChild; c!==null; c=c.nextSibling) {
      c.classList.remove("active")
    }
}

function createTextDiv(t) {
    const divNode = document.createElement("a");
    const text = document.createTextNode(t);
    divNode.className = "list-group-item list-group-item-action";
    divNode.appendChild(text);
    divNode.classList.add("clickable")
    return divNode;
}


window.onload = function () {
    col1 = document.getElementById("col1");
    col2 = document.getElementById("col2");
    col3 = document.getElementById("col3");

    for (const key in dataDict) {
        const divNode = createTextDiv(key);
        divNode.addEventListener("click", function () {
            clearSecondCol();
            clearThirdCol()
            divNode.classList.add("active")


            const elementsToAdd = dataDict[key];
            elementsToAdd.forEach(element => {
                const textElement = createTextDiv(element);
                textElement.addEventListener("click", function () {
                    clearThirdCol();
                    textElement.classList.add("active")
                    const clone = textElement.cloneNode(true)
                    col3.appendChild(clone);
                })
                col2.appendChild(textElement)
            });
        });
        col1.appendChild(divNode);
    }

};