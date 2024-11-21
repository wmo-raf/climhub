document.addEventListener("DOMContentLoaded", function () {
    const COUNTRY_CHOICES = [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
        "Cameroon", "Cape Verde", "Central African Republic", "Chad", "Comoros",
        "Congo - Brazzaville", "Congo - Kinshasa", "Côte d'Ivoire", "Djibouti", "Egypt",
        "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia",
        "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya",
        "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
        "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "São Tomé and Príncipe",
        "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
        "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
    ];

    // Apply Tagify to all CharBlock inputs named "countries"
    document.querySelectorAll('input[name="countries"]').forEach(input => {
        new Tagify(input, {
            whitelist: COUNTRY_CHOICES,
            dropdown: {
                maxItems: 10, // Show max 10 items in the dropdown
                enabled: 0    // Always show the dropdown when typing
            }
        });
    });
});
