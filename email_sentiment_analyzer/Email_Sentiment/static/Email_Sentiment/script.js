addEventListener("DOMContentLoaded", (event) => {

    console.log("Loaded");

    document.getElementById("submit").addEventListener("click", () => {submit_data()});
    
    document.getElementById("textInput").addEventListener("keydown", () => {
            document.getElementById("submit").disabled = false;
        })

})

async function submit_data(){

    text_content = document.getElementById("textInput").value
    
    if(text_content == ""){
        console.log("Please Input text before submitting")
        return false
    }

    let response = await fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': `${document.cookie.split('=').pop()}`
        },
        body: JSON.stringify({
            data: text_content,
        })
    });
    try {const result = await response.json()
     
        let sentences = result.sentences;
        let overall_sentiment = result.overall_sentiment
        let overall_sarcastic = result.overall_sarcastic

        let analysed_sentences = document.createElement("p")
        analysed_sentences.id = "returned"
          
        for (const [key, value] of Object.entries(sentences)) {
            const span = document.createElement("span");
            // const hoverspan = document.createElement("span");
            span.innerHTML = `${key}`;
            var sarcastic_note = "No";
            if(value[1] === "Sarcastic"){
                sarcastic_note = "Yes"
            }
            span.innerHTML += `<span class="hide"><p>Sentiment: ${value[2]}</p><p>Sarcastic: ${sarcastic_note}</p></span>`
            console.log(value[1]);
            span.classList.add(value[0], value[1], "analysedSpan");
            // hoverspan.classList.add("hide");
            analysed_sentences.appendChild(span);
            // analysed_sentences.appendChild(hoverspan);
        }

        if(document.getElementById("prereturn")){
            document.getElementById("prereturn").remove()}
        
        if(document.getElementById("returned")){
            document.getElementById("returned").remove()}
            
        

        document.getElementById("return").appendChild(analysed_sentences)

        document.getElementById("submit").disabled = true;

        document.getElementById("overall_sentiment").innerHTML = overall_sentiment
        document.getElementById("overall_sarcasm").innerHTML = overall_sarcastic
        
    }
    catch (error) {
       
        console.log("error")
    }
}
