const selectOption = (select, value) => {
    if (value == undefined) return;
    for (let i = 0; i < select.options.length; i++) {
        let currOption = select.options[i];

        if (currOption.value == value) {
            currOption.selected = true;
            break;
        }
    }
}

const getSelectedOption = select => {
    for (let i = 0; i < select.options.length; i++) {
        let option = select.options[i];
        if (option.selected) return option.value;
    }
}

const getSelectedOptions = select => {
    let selected = [];
    for (let i = 0; i < select.options.length; i++) {
        let option = select.options[i];
        if (option.selected) selected.push(option.value);
    }
    return selected;
}

const getCookie = name => {
    let cookie = {};
    document.cookie.split(';').forEach(function (el) {
        let [k, v] = el.split('=');
        cookie[k.trim()] = v;
    })
    return cookie[name];
}


const setDefaultOption = (select) => {
    for (let i = 0; i < select.options.length; i++) {
        let currentOption = select.options[i];

        if (currentOption.value == '') {
            currentOption.selected = true;
            break;
        }
    }
}

const title = word => {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

const removeKey = (property, obj) => {
    const { [property]: unused, ...rest } = obj;
    return rest;
}

const getKeyByValue = (object, value) => {
    return Object.keys(object).find(key => object[key] === value);
}

const isEmpty = obj => Object.keys(obj).length === 0;

const daysOfTheWeek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']