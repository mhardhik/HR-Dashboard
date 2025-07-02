// Example: draw pie chart of gender distribution

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('genderChart').getContext('2d');
    const genderData = JSON.parse(document.getElementById('gender-data').textContent);

    const data = {
        labels: genderData.map(item => item.gender),
        datasets: [{
            data: genderData.map(item => item.count),
            backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56'],
        }]
    };

    new Chart(ctx, {
        type: 'pie',
        data: data,
    });
});
