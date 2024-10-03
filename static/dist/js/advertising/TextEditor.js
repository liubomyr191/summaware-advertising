const optionsButtons = document.querySelectorAll(".option-button");
const advancedOptionButton = document.querySelectorAll(".adv-option-button");

const fontName = document.querySelector("#fontName");
const fontSizeRef = document.querySelector("#fontSize");
const writingArea = document.querySelector("#text-input");
const linkButton = document.querySelector("#createLink");

const alignButtons = document.querySelectorAll(".align");
const spacingButtons = document.querySelectorAll(".spacing");
const formatButtons = document.querySelectorAll(".format");
const scriptButtons = document.querySelectorAll(".script");

const text = document.querySelector('#text-input');

const fontList = [
    "Arial",
    "Verdana",
    "Times New Roman",
    "Garamond",
    "Georgia",
    "Courier New",
    "cursive",
];

//Initial Settings
const initializer = () => {
    //function calls for highlighting buttons
    //No highlights for link, unlink,lists, undo,redo since they are one time operations
    highlighter(alignButtons, true);
    highlighter(spacingButtons, true);
    highlighter(formatButtons, false);
    highlighter(scriptButtons, true);

    //create options for font names
    fontList.map((value) => {
        let option = document.createElement("option");
        option.value = value;
        option.innerHTML = value;
        fontName.appendChild(option);
    });

    //fontSize allows only till 7
    for (let i = 1; i <= 7; i++) {
        let option = document.createElement("option");
        option.value = i;
        option.innerHTML = i;
        fontSizeRef.appendChild(option);
    }

    //default size
    fontSizeRef.value = 3;
};

//main logic
const modifyText = (command, defaultUi, value) => {
    //execCommand executes command on selected text
    console.log(command, value)
    document.execCommand(command, defaultUi, value);
};

//For basic operations which don't need value parameter
optionsButtons.forEach((button) => {
    button.addEventListener("click", e => {
        e.preventDefault();

        modifyText(button.id, false, null);
    });
});

//options that require value parameter (e.g colors, fonts)
advancedOptionButton.forEach((button) => {
    button.addEventListener("change", e => {
        e.preventDefault();

        modifyText(button.id, false, button.value);
    });
});

// linkButton.addEventListener("click", () => {
//     let userLink = prompt("Enter a URL");
//     //if link has http then pass directly else add https
//     if (/http/i.test(userLink)) {
//         modifyText(linkButton.id, false, userLink);
//     } else {
//         userLink = "http://" + userLink;
//         modifyText(linkButton.id, false, userLink);
//     }
// });

//Highlight clicked button
const highlighter = (className, needsRemoval) => {
    className.forEach((button) => {
        button.addEventListener("click", () => {
            if (needsRemoval) {
                let alreadyActive = false;

                //If currently clicked button is already active
                if (button.classList.contains("active-btn")) {
                    alreadyActive = true;
                }

                //Remove highlight from other buttons
                highlighterRemover(className);
                if (!alreadyActive) {
                    //highlight clicked button
                    button.classList.add("active-btn");
                }
            } else {
                //if other buttons can be highlighted
                button.classList.toggle("active-btn");
            }
        });
    });
};

const highlighterRemover = (className) => {
    className.forEach((button) => {
        button.classList.remove("active-btn");
    });
};

window.onload = initializer();