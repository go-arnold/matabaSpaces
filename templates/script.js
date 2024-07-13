//metre a jour ma page html qui contient les parkings
<script type="text/javascript">
    function fetchData() {
        $.ajax({
            url: 'http://127.0.0.1:8000/parking/', // L'URL de la vue Django qui renvoie les données des capteurs
            type: 'GET', // Utilisez 'GET' pour récupérer des données
            success: function(slots) {
                // Mettez à jour votre page avec les données reçues
                // par exemple, si vous avez une liste d'emplacements de parking :
                $('1').text(slots.slot1);
                $('2').text(slots.slot2);
                $('3').text(slots.slot3);
                $('4').text(slots.slot4);
                // Répétez pour chaque slot ou données que vous avez
            }
        })//;
    }

    
    setInterval(fetchData, 5000);
</script>
////Appeler fetchData() toutes les 5 secondes pour une mise à jour en temps réel