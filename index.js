  document.getElementById('registrationForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data - matching your Lambda function's expected format
        const formData = {
            Name: document.getElementById('name').value,
            Age: document.getElementById('age').value,
            Email: document.getElementById('email').value,
            EventName: document.getElementById('event').value
        };
        
        try {
            const API_URL = 'https://epwyrdamt0.execute-api.ap-south-1.amazonaws.com/development/register';
            
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const responseData = await response.json();
            
            if (response.ok) {
                // Show success message
                document.getElementById('successMessage').style.display = 'block';
                document.getElementById('successMessage').textContent = 'Registration successful! Thank you for registering.';
                document.getElementById('successMessage').style.backgroundColor = '#d4edda';
                document.getElementById('successMessage').style.color = '#155724';
                document.getElementById('successMessage').style.borderColor = '#c3e6cb';
                
                
                // Reset form after a delay
                setTimeout(() => {
                    document.getElementById('registrationForm').reset();
                    document.getElementById('successMessage').style.display = 'none';
                }, 5000);
            } else {
                throw new Error(responseData.error || 'Registration failed');
            }
        } catch (error) {
            // Show error message
            document.getElementById('successMessage').style.display = 'block';
            document.getElementById('successMessage').textContent = 'Registration failed: ' + error.message;
            document.getElementById('successMessage').style.backgroundColor = '#f8d7da';
            document.getElementById('successMessage').style.color = '#721c24';
            document.getElementById('successMessage').style.borderColor = '#f5c6cb';
            
            console.error('Error:', error);
            
            // Hide error message after delay
            setTimeout(() => {
                document.getElementById('successMessage').style.display = 'none';
            }, 5000);
        }
    });
    // Add smooth focus effects
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });