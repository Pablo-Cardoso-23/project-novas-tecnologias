function filtrarDados() {

    const br = document.getElementById("br").value;
    const tipo_acidente = document.getElementById("tipo_acidente").value;
    const ano = document.getElementById("ano").value;

    fetch(`/dados_ocorrencias?br=${br}&tipo_acidente=${tipo_acidente}&ano=${ano}`)
    .then(response => response.json())
    .then(data => {
    console.log("Dados recebidos:", data);
        atualizarDashboard(data);
    })
    .catch(error => console.error("Erro ao buscar dados:  ", error));

}

function atualizarDashboard(data) {

    console.log("Dados filtrados recebidos: ", data);

    const ctx = document.getElementById('graficoOcorrencias').getContext('2d');

    if (Chart.getChart("graficoOcorrencias")) {

        Chart.getChart("graficoOcorrencias").destroy();
    }

    const labels = data.map(item => `BR-${item.br}`);
    const valores = data.map(item => parseInt(item.quantidade) || 0);

    console.log("Valores finais para o gráfico: ",  valores);

    if (valores.every(v => v === 0)) {

        alert("Nenhum dado encontrado para esse filtro.");

        return;
    }

    new Chart(ctx, {

        type: 'bar',
        data: {

            labels: labels,
            datasets: [{

                label: 'Acidentes nas BR',
                data: valores,
                backgroundColor: 'rgba(75, 192, 192, 0.7)',
                borderColor: 'white',
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            },
            scales: {

                x: {
                    grid: {
                        color: 'white'
                    },
                    ticks: {
                        color: 'white'
                    }
                },

                y: {

                    grid: {

                        color: 'white'
                    },
                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    });
}
