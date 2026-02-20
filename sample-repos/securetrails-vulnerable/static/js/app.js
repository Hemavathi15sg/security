// VULNERABILITY 1: eval() usage
function executeCustomCode(code) {
    eval(code);  // DANGEROUS - allows arbitrary code execution
}

// VULNERABILITY 2: Insecure API calls
async function fetchTrails() {
    const response = await fetch('/trails');
    const data = await response.json();
    
    // VULNERABILITY 3: Direct innerHTML manipulation
    data.forEach(trail => {
        const div = document.createElement('div');
        div.innerHTML = `
            <h3>${trail.name}</h3>
            <p>${trail.description}</p>  <!-- XSS if data contains HTML -->
        `;
        document.body.appendChild(div);
    });
}

// VULNERABILITY 4: Sensitive data in console
console.log('DEBUG: JWT Token = ' + localStorage.getItem('jwt_token'));
console.log('DEBUG: User Password Hash = ' + sessionStorage.getItem('pwd_hash'));

// VULNERABILITY 5: Missing CSRF protection
function submitForm(data) {
    fetch('/api/actions', {
        method: 'POST',
        body: JSON.stringify(data)
        // Missing: CSRF token
    });
}
