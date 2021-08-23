function getSolver() {
    components = document.getElementById("components").value;
    components = components.split(',');

    target = document.getElementById("target").value;

    configs = document.getElementById("configs").value === "s" ? 1 : 0;

    tolerance = document.getElementById("tolerance").value;

    component = document.getElementById("component").value === "r/i" ? 1 : 0;

    output = document.getElementById("output");
    postData('https://jsonplaceholder.typicode.com/todos/1',
        { components, target, configs, tolerance, component })
        .then(data => {
            output.innerHTML = data;
        });
}

async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}