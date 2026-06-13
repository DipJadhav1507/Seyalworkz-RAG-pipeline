const BASE_URL = "http://127.0.0.1:8000";

async function uploadFile() {

    const userId = document.getElementById("userId").value;
    const file = document.getElementById("csvFile").files[0];

    if (!userId || !file) {
        alert("Enter user id and select file");
        return;
    }

    const formData = new FormData();

    formData.append("user_id", userId);
    formData.append("file", file);

    try {

        const response = await fetch(
            `${BASE_URL}/upload`,
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        document.getElementById("uploadStatus")
            .innerText = data.message;

    }
    catch(error){

        console.error(error);

        document.getElementById("uploadStatus")
            .innerText = "Upload Failed";
    }
}

async function analyzeData() {

    const userId = document.getElementById("userId").value;

    const query = document.getElementById("query").value;

    if(!userId || !query){
        alert("Enter user id and query");
        return;
    }

    document.getElementById("report")
        .innerText = "Generating report...";

    try{

        const response = await fetch(
            `${BASE_URL}/analyze`,
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    user_id:userId,
                    query:query
                })
            }
        );

        const data = await response.json();

        document.getElementById("report")
            .innerText = data.report;

    }
    catch(error){

        console.error(error);

        document.getElementById("report")
            .innerText = "Error generating report";
    }
}