const textContent = document.getElementById("textContent");
const numerator = ["NN", "PM", "PP", "PC"];
const denominator = ["PN", "PS", "VB", "AB"];

const params = new URLSearchParams(window.location.search);
let currentModel = params.get("model") || Object.keys(dataFile)[0];
let currentFile = params.get("fileID") || 0 
let currentTextID = params.get("textID") || 0;
updateURL();
setSettingsVisuals();

renderSentences();

// store application states in url since refreshing is great but losing your state isn't.
function updateURL() {
    // const newUrl = `?model=${encodeURIComponent(currentModel)}&textID=${encodeURIComponent(currentTextID)}`;
    const newUrl = `?model=${encodeURIComponent(currentModel)}&fileID=${encodeURIComponent(currentFile)}&textID=${encodeURIComponent(currentTextID)}`;
    window.history.pushState(null, '', newUrl);
}

// settings-related things
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
        updateURL();
        setSettingsVisuals(); // update the text options to match current model (in case they have anaylized different corpuses)
        renderSentences();
    }


    if (settingElement.name == "fileID") {
        if (dataFile[currentModel].length-1 < settingElement.value) {
            alert("Något gick snett");
            return;
        }
        currentFile = settingElement.value;
        updateURL();
        setSettingsVisuals();
        renderSentences();
    };


    if (settingElement.name == "textID") {
        if (dataFile[currentModel][currentFile].texts.length-1 < settingElement.value) {
            alert("Den här texten har inte analyserats med den modell som är vald.");
            return;
        }
        currentTextID = settingElement.value;
        updateURL();
        setSettingsVisuals();
        renderSentences();
    }
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
}

function renderSentences() {
    const sentences = dataFile[currentModel][currentFile].texts[currentTextID].sentences
    let countNouns = 0;
    let countVerbs = 0;
    let inQuote = false;

    textContent.innerText = "";
    for (sentence of sentences) {
        const sentenceElement = document.createElement("div");
        sentenceElement.classList = "sentence"
        for (let i=0; i < sentence.length; i++) {
            const word = sentence[i]

            const wordDiv = document.createElement("div");
            wordDiv.classList = "tooltip";
            wordDiv.innerText = word.word;

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


            if (inQuote)
                wordDiv.classList+=" quoted";

            if (word.word == '"') {
                if (!inQuote) // also mark the very first quoted token (the quotation mark) as quoted
                    wordDiv.classList+=" quoted";
                inQuote = !inQuote;
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
    document.getElementById("fullNominalQuotient").innerText = "Full nominalkvot: " + currentText.full_nominal_quotient;
    document.getElementById("simpleNominalQuotient").innerText = "Enkel nominalkvot: " + currentText.simple_nominal_quotient;
    document.getElementById("wordCount").innerText = "Antal ord: " + currentText.word_count;
    document.getElementById("meanSentenceLength").innerText = "Genomsnittlig meningslängd: " + currentText.mean_sentence_length;
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