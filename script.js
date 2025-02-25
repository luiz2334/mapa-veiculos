const API_URL = "http://127.0.0.1:5000/api/vehicles"; // URL da API Flask
let map = L.map("map").setView([-22.9, -43.2], 12);
let markers = L.layerGroup().addTo(map);
let intervaloTempoReal = null;

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

document.getElementById("btnTempoReal").addEventListener("click", ativarModoTempoReal);
document.getElementById("btnHistorico").addEventListener("click", ativarModoHistorico);
document.getElementById("buscarHistorico").addEventListener("click", buscarHistorico);

function ativarModoTempoReal() {
    clearInterval(intervaloTempoReal);
    document.getElementById("historicoDataHora").style.display = "none";
    document.getElementById("buscarHistorico").style.display = "none";
    atualizarMapaTempoReal();
    intervaloTempoReal = setInterval(atualizarMapaTempoReal, 10000);
}

function ativarModoHistorico() {
    clearInterval(intervaloTempoReal);
    document.getElementById("historicoDataHora").style.display = "block";
    document.getElementById("buscarHistorico").style.display = "block";
}

function atualizarMapaTempoReal() {
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            atualizarMarcadores(data);
        })
        .catch(error => console.error("Erro ao buscar dados:", error));
}

function buscarHistorico() {
    let dataHora = document.getElementById("historicoDataHora").value;
    if (!dataHora) {
        alert("Selecione uma data e hora!");
        return;
    }
    
    let [data, hora] = dataHora.split("T");
    fetch(`${API_URL}?data=${data}&hora=${hora}`)
        .then(response => response.json())
        .then(data => {
            atualizarMarcadores(data);
        })
        .catch(error => console.error("Erro ao buscar dados históricos:", error));
}

function atualizarMarcadores(veiculos) {
    markers.clearLayers();
    veiculos.forEach(veiculo => {
        let marker = L.marker([veiculo.latitude, veiculo.longitude]).bindPopup(`
            <b>Linha:</b> ${veiculo.lineid} <br>
            <b>Carro:</b> ${veiculo.carnbr} <br>
            <b>Horário:</b> ${veiculo.rtcdatetime}
        `);
        markers.addLayer(marker);
    });
}
