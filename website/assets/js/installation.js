const locationScriptContainer = document.getElementById("location-script-container");
const locationScript = `cat /dev/location > /dev/null &`;
locationScriptContainer.innerHTML = Prism.highlight(locationScript, Prism.languages.bash, "bash");

const installScriptContainer = document.getElementById("install-script-container");
const installScript = `apk add curl && curl -fsSL https://raw.githubusercontent.com/ManoahKinnaert/CLMMobile/main/install_ish.sh | ash`;
installScriptContainer.innerHTML = Prism.highlight(installScript, Prism.languages.bash, "bash");

const launchScriptContainer = document.getElementById("launch-script-container");
const launchScript = `timer`;
launchScriptContainer.innerHTML = Prism.highlight(launchScript, Prism.languages.bash, "bash");