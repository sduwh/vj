function setSelectedOption(selectId, optionValue) {
    var s = document.getElementById(selectId);
    for (var i = 0; i < s.length; i++) {
        if (optionValue == s.options[i].text) {
            s.selectedIndex = i;
            break;
        }
    }
}