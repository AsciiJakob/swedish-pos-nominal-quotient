const textContent = document.getElementById("textContent");
const numerator = ["NN", "PM", "PP", "PC"];
const denominator = ["PN", "PS", "VB", "AB"];

const params = new URLSearchParams(window.location.search);
let currentModel = params.get("model") || Object.keys(dataFile)[0];
let currentFile = params.get("fileID") || 0 
let currentTextID = params.get("textID") || 0;
if (dataFile[currentModel] == undefined) {
    currentModel = Object.keys(dataFile)[0];
}
if (dataFile[currentModel][currentFile] == undefined) {
    currentFile = 0;
    currentTextID = 0;
}
let markIgnored = params.get("markIgnored");
console.log(markIgnored)
if (markIgnored == undefined) {
    markIgnored = true // default value
} else {
    markIgnored = markIgnored === "true";
}
let loadPythonFiltering = params.get("pythonFiltering") === "true";
if (loadPythonFiltering == undefined)
    loadPythonFiltering = false
updateURL();
setSettingsVisuals();
renderSentences();

// store application states in url since refreshing is great but losing your state isn't.
function updateURL() {
    // const newUrl = `?model=${encodeURIComponent(currentModel)}&textID=${encodeURIComponent(currentTextID)}`;
    const newUrl = `?model=${encodeURIComponent(currentModel)}&fileID=${encodeURIComponent(currentFile)}&textID=${encodeURIComponent(currentTextID)}&markIgnored=${encodeURIComponent(markIgnored)}&pythonFiltering=${encodeURIComponent(loadPythonFiltering)}`;
    window.history.pushState(null, '', newUrl);
}

// settings-related things
let lastMarkIgnoredValue = markIgnored
document.getElementById("settingsContainer").addEventListener("change", mouseEvent => handleSetting(mouseEvent.target));
function handleSetting(settingElement) {
    if (settingElement.name == "model") {
        if (dataFile[settingElement.id] == undefined) {
            document.getElementById(currentModel).checked = true;
            alert("Det finns ingen data från modellen i datafilen.");
            return;
        }
        if (dataFile[settingElement.id][currentFile].texts.length-1 < currentTextID) {
                // alert("Den för närvarande valda texten har inte analyserats med denna modell.");
                // doment.getElementById(currentModel).checked = true;
                // return;
                currentTextID = 0;
        }
        currentModel = settingElement.id;
    } else if (settingElement.name == "fileID") {
        if (dataFile[currentModel].length-1 < settingElement.value) {
            alert("Något gick snett");
            return;
        }
        currentFile = settingElement.value;

    } else if (settingElement.name == "textID") {
        if (dataFile[currentModel][currentFile].texts.length-1 < settingElement.value) {
            alert("Den här texten har inte analyserats med den modell som är vald.");
            return;
        }
        currentTextID = settingElement.value;

    } else if (settingElement.name == "markIgnored") {
        markIgnored = settingElement.checked;

    } else if (settingElement.name == "loadPythonFiltering") {
        loadPythonFiltering = settingElement.checked;
        if (settingElement.checked) {
            lastMarkIgnoredValue = markIgnored
            markIgnored = false;
        } else {
            markIgnored = lastMarkIgnoredValue
        }

    }
    updateURL();
    setSettingsVisuals();
    renderSentences();
}

function setSettingsVisuals() {

    // add file names
    const fileSelector = document.getElementById("fileSelector");
    let oldValue = fileSelector.value;
    if (!oldValue)
        oldValue = currentFile || 0;
    fileSelector.innerText = "";
    for (fileIndex in dataFile[currentModel]) {
        const file = dataFile[currentModel][fileIndex];
        fileOption = document.createElement("option");
        fileOption.value = fileIndex;
        fileOption.name = "fileID";
        fileOption.innerText = file.filename;
        fileSelector.appendChild(fileOption);
    }
    console.log("setting value to", oldValue);
    fileSelector.value = oldValue;


    // add texts
    const textSelector = document.getElementById("textSelector");
    textSelector.innerText = "";
    for (textIndex in dataFile[currentModel][currentFile].texts) {
        const text = dataFile[currentModel][currentFile].texts[textIndex];
        textOption = document.createElement("option");
        textOption.value = textIndex;
        textOption.name = "textID";
        textOption.innerText = text.id;
        textSelector.appendChild(textOption);
    }

    
    // add models
    const modelSelector = document.getElementById("modelSelector");
    modelSelector.innerText = "";
    const legend = document.createElement("legend");
    legend.innerText = "Ordklasstaggningsmodell:"
    modelSelector.appendChild(legend);
    for (modelName of Object.keys(dataFile)) {
        const modelElement = document.createElement("input");
        modelElement.id = modelName;
        modelElement.name = "model";
        modelElement.type = "radio";

        const modelLabel = document.createElement("label");
        modelLabel.innerText = modelName;
        modelLabel.htmlFor = modelName;

        modelSelector.appendChild(modelElement);
        modelSelector.appendChild(modelLabel);
    }

    // set the models radio dial to selected 
    document.getElementById(currentModel).checked = true;

    document.getElementById("textSelector").value = currentTextID;

    document.getElementById("markIgnored").checked = markIgnored;
    document.getElementById("loadPythonFiltering").checked = loadPythonFiltering;
    document.getElementById("markIgnored").disabled = loadPythonFiltering;
}


function checkTokens(sentence, base, ...args) {
    for (let i=0; i < args.length; i++) {
        if (sentence[base+i]["word"] != args[i])
            return false
    }
    return true
}

function renderSentences() {
    let sentences = []
    let renderText = dataFile[currentModel][currentFile].texts[currentTextID]
    if (renderText == undefined) {
        currentFile = 0;
        currentTextID = 0;
        renderText = dataFile[currentModel][currentFile].texts[currentTextID];
    }
    if (loadPythonFiltering) {
        sentences = renderText.filtered_sentences;
    } else {
        sentences = renderText.sentences;
    }
    let countNouns = 0;
    let countVerbs = 0;
    let inQuote = false;
    let inItalics = false;
    let parenthesisDepth = 0;

    textContent.innerText = "";
    for (sentence of sentences) {
        const sentenceElement = document.createElement("div");
        sentenceElement.classList = "sentence"
        for (let i=0; i < sentence.length; i++) {
            const word = sentence[i]

            const wordDiv = document.createElement("div");
            wordDiv.classList = "tooltip";
            wordDiv.innerText = word.word;

            
            if (markIgnored) {
                if (inQuote || parenthesisDepth != 0)
                    wordDiv.classList+=" ignored";

                if (word.word == '"') {
                    if (!inQuote) // also mark the very first quoted token (the quotation mark) as quoted
                        wordDiv.classList+=" ignored";
                    inQuote = !inQuote;
                } else if (word.word == '(') {
                    if (parenthesisDepth == 0)
                        wordDiv.classList+=" ignored";
                    parenthesisDepth += 1;
                } else if (word.word == ')') {
                    parenthesisDepth -= 1;
                } else if (checkTokens(sentence, i, '{', '\\', "ITALICS", '}')) {
                    inItalics = false;
                    wordDiv.remove();
                    i += 3; // skip this and the next 3 tokens
                    continue;
                } else if (checkTokens(sentence, i, '{', "ITALICS", '}')) {
                    inItalics = true;
                    wordDiv.remove();
                    i += 2; // skip this and the next 2 tokens
                    continue;
                }

                if (inItalics)
                    wordDiv.classList+= " italics ignored"
            }

            if (markIgnored | (!inQuote && !inItalics && parenthesisDepth == 0)) {
                if (numerator.includes(word.entity_group)) {
                    wordDiv.classList+=" numerator"
                }
                if (denominator.includes(word.entity_group)) {
                    wordDiv.classList+=" denominator"
                }

                if (word.entity_group == "NN")
                    countNouns++;
                if (word.entity_group == "VB")
                    countVerbs++;
            }

            const tooltip = document.createElement("span");
            tooltip.classList = "tooltipText";
            tooltip.innerText = word.entity_group;
            const full = fullTagName(word.entity_group);
            if (full != undefined)
                tooltip.innerText += ": "+full;
            
            
            wordDiv.appendChild(tooltip);
            sentenceElement.appendChild(wordDiv);
            if (i != sentence.length-1 && sentence[i+1].entity_group != "MAD") {
                sentenceElement.innerHTML += " "
            }
        }
        textContent.appendChild(sentenceElement);

        const spacer = document.createElement("br");
        textContent.appendChild(spacer);
    }

    // set metric values
    const currentText = dataFile[currentModel][currentFile].texts[currentTextID];
    document.getElementById("verbNounCount").innerText = "Verb: "+countVerbs+" substantiv: "+countNouns;
    document.getElementById("fullNominalQuotient").innerText = "Full nominalkvot: " + currentText.full_nominal_quotient.toFixed(3);
    document.getElementById("simpleNominalQuotient").innerText = "Enkel nominalkvot: " + currentText.simple_nominal_quotient.toFixed(3);
    document.getElementById("wordCount").innerText = "Antal tokens: " + currentText.word_count;
    document.getElementById("meanSentenceLength").innerText = "Genomsnittlig meningslängd: " + currentText.mean_sentence_length.toFixed(2);
    document.getElementById("quoteCharCount").innerText = "Antal citattecken: " + currentText.quote_char_count;
    document.getElementById("quoteRatio").innerText = "Andel tokens inom citat: " + (currentText.quote_ratio*10).toFixed(2) + "%";
    document.getElementById("lix").innerText = "LIX-värde: " + (currentText.LIX).toFixed(2);
    document.getElementById("ovix").innerText = "OVIX-värde: " + (currentText.OVIX).toFixed(2);
}



function fullTagName(tag) {
// generated by gpt
    const tagMapping = {
        'AB': 'Adverb',
        'DT': 'Determinerare',
        'HA': 'Frågande/relativt adverb',
        'HD': 'Frågande/relativt determinera',
        'HP': 'Frågande/relativt pronomen',
        'HS': 'Frågande/relativt possessivt pronomen',
        'IE': 'Infinitivmärke',
        'IN': 'Interjektion',
        'JJ': 'Adjektiv',
        'KN': 'Konjunktion',
        'NN': 'Substantiv',
        'PC': 'Particip',
        'PL': 'Partikel',
        'PM': 'Egenamn',
        'PN': 'Pronomen',
        'PP': 'Preposition',
        'PS': 'Possessivt pronomen',
        'RG': 'Grundtal',
        'RO': 'Ordningstal',
        'SN': 'Subjunktion',
        'UO': 'Utländskt ord',
        'VB': 'Verb'
    };

    return tagMapping[tag] || undefined;
}