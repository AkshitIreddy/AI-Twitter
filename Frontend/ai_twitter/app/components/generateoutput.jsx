export const generateOutput = async (
  setLoading,
  setpostData
) => {
  const headers = new Headers();
  headers.append("Content-Type", "application/json");
  headers.append("Authorization", "Basic " + btoa("myusername:mypassword"));

  const message = "start";
  const body = JSON.stringify({
    message,
  });

  const response = await fetch("http://127.0.0.1:8000/inference", {
    method: "POST",
    body: body,
    headers: headers,
  });

  if (response.ok) {
    const jsonData = await response.json();
    const result = jsonData; 
    setpostData(result);
    console.log("Success");
  } else {
    console.log("Error:", response.statusText);
  }
  
  setLoading(false);
};
