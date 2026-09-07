document.addEventListener('DOMContentLoaded', function() {
    const sectorSelect = document.getElementById('sector');
    const companySelect = document.getElementById('company');
    const stressOptions = document.getElementById('stress-options');

    sectorSelect.addEventListener('change', function() {
        const sector = this.value;
        const companies = {
            'IT': ['Google', 'Apple', 'Intel', 'Microsoft', 'Nvidia'],
            'Finance': ['Bank of America', 'Berkshire Hathaway', 'Goldman Sachs', 'JPMorgan', 'Wells Fargo'],
            'Healthcare': ['Abbvie', 'Johnson & Johnson', 'Merck', 'Pfizer', 'UnitedHealth'],
            'Real Estate': ['AvalonBay', 'Prologis Inc', 'Public Storage', 'Realty Income', 'Simon Property'],
            'Energy': ['Chevron Corporation', 'ConocoPhillips', 'Exxon Mobil', 'NextEra', 'Schlumberger']
        };

        companySelect.innerHTML = '<option value="" disabled selected>Select Company</option>';
        if (sector in companies) {
            companies[sector].forEach(company => {
                const option = document.createElement('option');
                option.value = company;
                option.textContent = company;
                companySelect.appendChild(option);
            });
        }
    });

    const operationSelect = document.getElementById('operation');
    operationSelect.addEventListener('change', function() {
        if (this.value === 'stress_test') {
            stressOptions.style.display = 'block';
        } else {
            stressOptions.style.display = 'none';
        }
    });
});
