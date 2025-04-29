document.addEventListener('DOMContentLoaded', function() {
    const bmiForm = document.getElementById('bmiForm');
    const bmrForm = document.getElementById('bmrForm');
    const API_URL = 'http://localhost:5000/api';

    // Gestion du calcul IMC
    bmiForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const height = parseFloat(document.getElementById('bmiHeight').value);
        const weight = parseFloat(document.getElementById('bmiWeight').value);

        try {
            const response = await fetch(`${API_URL}/bmi`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ height, weight })
            });

            const data = await response.json();
            const resultBox = document.getElementById('bmiResult');
            const resultValue = resultBox.querySelector('.result-value');
            const resultInterpretation = resultBox.querySelector('.result-interpretation');

            if (response.ok) {
                resultBox.classList.remove('d-none');
                resultValue.textContent = `IMC: ${data.bmi.toFixed(2)}`;
                resultInterpretation.textContent = getIMCInterpretation(data.bmi);
            } else {
                resultBox.classList.remove('d-none');
                resultValue.textContent = 'Erreur';
                resultInterpretation.textContent = data.error;
            }
        } catch (error) {
            console.error('Erreur:', error);
        }
    });

    // Gestion du calcul BMR
    bmrForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const height = parseFloat(document.getElementById('bmrHeight').value);
        const weight = parseFloat(document.getElementById('bmrWeight').value);
        const age = parseInt(document.getElementById('bmrAge').value);
        const gender = document.getElementById('bmrGender').value;

        try {
            const response = await fetch(`${API_URL}/bmr`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ height, weight, age, gender })
            });

            const data = await response.json();
            const resultBox = document.getElementById('bmrResult');
            const resultValue = resultBox.querySelector('.result-value');
            const resultInterpretation = resultBox.querySelector('.result-interpretation');

            if (response.ok) {
                resultBox.classList.remove('d-none');
                resultValue.textContent = `BMR: ${Math.round(data.bmr)} calories/jour`;
                resultInterpretation.textContent = getBMRInterpretation(data.bmr);
            } else {
                resultBox.classList.remove('d-none');
                resultValue.textContent = 'Erreur';
                resultInterpretation.textContent = data.error;
            }
        } catch (error) {
            console.error('Erreur:', error);
        }
    });

    // Fonction d'interprétation de l'IMC
    function getIMCInterpretation(bmi) {
        if (bmi < 18.5) return 'Insuffisance pondérale';
        if (bmi < 25) return 'Corpulence normale';
        if (bmi < 30) return 'Surpoids';
        if (bmi < 35) return 'Obésité modérée';
        if (bmi < 40) return 'Obésité sévère';
        return 'Obésité morbide';
    }

    // Fonction d'interprétation du BMR
    function getBMRInterpretation(bmr) {
        return `Votre métabolisme de base est de ${Math.round(bmr)} calories par jour. ` +
               `C'est le nombre minimum de calories dont votre corps a besoin pour fonctionner au repos.`;
    }
}); 