function getSolver() {
    components = document.getElementById("components").value;
    components = components.split(',');

    target = document.getElementById("target").value;

    configs = document.getElementById("configs").value === "s" ? 1 : 0;

    tolerance = document.getElementById("tolerance").value;

    component = document.getElementById("component").value === "r/i" ? 1 : 0;

    output = document.getElementById("output");
    postData('https:localhost:5000/',
        { components, target, configs, tolerance, component })
        .then(data => {
            output.innerHTML = data;
        });
}

async function postData(url = '', data = {}) {
                                            // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST',                     // *GET, POST, PUT, DELETE, etc.
        body: JSON.stringify(data)          // body data type must match "Content-Type" header
    });
    return response.json();                  // parses JSON response into native JavaScript objects
}