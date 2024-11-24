document.addEventListener('DOMContentLoaded', () => {
    const agePrompt = document.getElementById('age-prompt');
    const message = document.getElementById('message');
    
    // Check if the date of birth is already stored
    const storedDOB = localStorage.getItem('dob');
    if (!storedDOB) {
        agePrompt.style.display = 'flex';  // Show prompt if DOB is not stored
    }
});

function submitDOB() {
    const dobInput = document.getElementById('dob').value;
    if (dobInput) {
        const dob = new Date(dobInput);
        localStorage.setItem('dob', dobInput);
        displayMessage(dob);
    } else {
        alert('Please enter a valid date.');
    }
}

function displayMessage(dob) {
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();

    // Adjust for the day of the year if not yet birthday this year
    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
        age--;
    }

    const dayOfWeek = dob.toLocaleDateString('en-US', { weekday: 'long' });
    let messageContent = `You were born on a ${dayOfWeek}.\nYou are ${age} years old.`;

    if (age < 18) {
        alert('You need parental permission to use this site.');
        localStorage.removeItem('dob')
        window.open("https://mini.ya.ru", "_self")
    } else {
        alert(messageContent)
        document.getElementById('age-prompt').style.display = 'none';
    }
    // s
}