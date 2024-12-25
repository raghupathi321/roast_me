// Define the TimelessDebugger ASCII art
const timelessDebuggerBanner = `
████████╗██╗███╗   ███╗███████╗██╗     ███████╗███████╗███████╗    ██████╗ ███████╗██████╗ ██╗   ██╗ ██████╗  ██████╗ ███████╗██████╗ 
╚══██╔══╝██║████╗ ████║██╔════╝██║     ██╔════╝██╔════╝██╔════╝    ██╔══██╗██╔════╝██╔══██╗██║   ██║██╔════╝ ██╔════╝ ██╔════╝██╔══██╗
   ██║   ██║██╔████╔██║█████╗  ██║     █████╗  ███████╗███████╗    ██║  ██║█████╗  ██████╔╝██║   ██║██║  ███╗██║  ███╗█████╗  ██████╔╝
   ██║   ██║██║╚██╔╝██║██╔══╝  ██║     ██╔══╝  ╚════██║╚════██║    ██║  ██║██╔══╝  ██╔══██╗██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
   ██║   ██║██║ ╚═╝ ██║███████╗███████╗███████╗███████║███████║    ██████╔╝███████╗██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝╚══════╝╚══════╝    ╚═════╝ ╚══════╝╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                                                        
`;

// Insert the ASCII banner into the pre tag with the id 'ascii-banner'
document.getElementById('ascii-banner').textContent = timelessDebuggerBanner;

// Function to fetch and display roast for the entered username
function getRoast() {
    const username = document.getElementById('username').value;
    const roastResult = document.getElementById('roast-result');

    // Validate that the username is not empty
    if (username.trim() === "") {
        roastResult.textContent = "Please enter a username!";
        return;
    }

    // Make the POST request to the Flask backend
    fetch('http://127.0.0.1:5000/roast', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        // Display the roast or an error message if not available
        roastResult.textContent = data.roast || "Error: Something went wrong!";
    })
    .catch(error => {
        // Handle any errors from the request
        roastResult.textContent = "Error: Unable to fetch roast.";
        console.error('Error:', error);
    });
}
