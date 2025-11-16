// API Configuration
const API_CONFIG = {
    backendUrl: 'http://localhost:3000'
};

/**
 * Analyze symptoms using the backend API
 * @param {string} symptoms - User's symptom description
 * @returns {Promise<Object>} Analysis result
 */
async function analyzeSymptoms(symptoms) {
    if (!symptoms || typeof symptoms !== 'string' || symptoms.trim().length === 0) {
        throw new Error('Please enter your symptoms.');
    }

    try {
        const response = await fetch(`${API_CONFIG.backendUrl}/api/analyze-symptoms`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                symptoms: symptoms.trim()
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            
            if (response.status === 500 && errorData.error?.includes('API key')) {
                throw new Error('Backend API key not configured. Please check backend .env file.');
            } else if (response.status === 503) {
                throw new Error('Service temporarily unavailable. Please try again later.');
            } else if (response.status === 429) {
                throw new Error('Rate limit exceeded. Please wait a moment and try again.');
            } else {
                throw new Error(errorData.error || `Server error: ${response.status}`);
            }
        }

        const result = await response.json();
        
        // Handle backend errors
        if (result.error) {
            throw new Error(result.error);
        }
        
        // Handle non-medical queries
        if (result.is_medical_query === false) {
            return result;
        }
        
        // If no is_medical_query field but has response, treat as non-medical
        if (result.response && !result.possible_conditions) {
            return {
                is_medical_query: false,
                response: result.response
            };
        }
        
        // If there are no medical fields at all, treat as conversational
        if (!result.possible_conditions && !result.severity && !result.recommendations && !result.see_doctor) {
            return {
                is_medical_query: false,
                response: result.response || result.message || 'I understand. Could you please describe any specific symptoms you\'re experiencing?'
            };
        }
        
        // Validate medical response structure
        if (result.possible_conditions || result.severity || result.recommendations) {
            // If partially complete, fill in defaults
            if (!result.possible_conditions || !result.severity || !result.recommendations || !result.see_doctor) {
                return {
                    is_medical_query: true,
                    possible_conditions: result.possible_conditions || ['Unable to determine - please consult a healthcare professional'],
                    severity: result.severity || 'Medium',
                    recommendations: result.recommendations || 'Please consult a healthcare professional for proper evaluation',
                    see_doctor: result.see_doctor || 'It is recommended to consult a healthcare professional for proper medical evaluation'
                };
            }
        }

        return result;

    } catch (error) {
        if (error instanceof TypeError && error.message.includes('fetch')) {
            throw new Error('Cannot connect to backend server. Make sure the backend is running on http://localhost:3000');
        }
        throw error;
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { analyzeSymptoms };
}
