function openTab(evt, tabName) {
    var i, tabcontent, tabbuttons;
    tabcontent = document.getElementsByClassName("proposals-tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].className = tabbuttons[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    sessionStorage.setItem('activeProposalTab', tabName);
}

document.addEventListener('DOMContentLoaded', function() {
    var activeTab = sessionStorage.getItem('activeProposalTab') || 'received-proposals';
    document.getElementById(activeTab).style.display = "block";
    var buttons = document.getElementsByClassName("tab-button");
    for (var i = 0; i < buttons.length; i++) {
        if (buttons[i].getAttribute('onclick').includes(activeTab)) {
            buttons[i].className += " active";
        }
    }
});
