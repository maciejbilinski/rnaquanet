import { useEffect, useState } from "react";
import { Box, CircularProgress, Typography } from "@mui/material";

import { API_ADDRESS, REQUEST_RETRY_DELAY } from "../../../../config";

const CheckRmsd = () => {
  const [response, setResponse] = useState<ICheckRmsd>({});

  const fetchData = async () => {
    try {
      const res = await fetch(`${API_ADDRESS}/check_rmsd${location.pathname}`, {
        method: "GET",
      });

      // if the API responded correctly, parse received data
      let json: ResponseCheckRmsd = {};
      if (res.status === 200) {
        json = await res.json();
      }
      setResponse({
        status: json.status,
        results: json.results,
        reqStatus: res.status,
      });

      if (res.status === 200 && json.status !== "DONE") {
        setTimeout(fetchData, REQUEST_RETRY_DELAY);
      }
    }
    catch (error) {
      setResponse({
        reqStatus: 500,
      });
      console.error(error);
      setTimeout(fetchData, REQUEST_RETRY_DELAY);
    }
  };

  const getMessage = () => {
    // if (response.) return <CircularProgress size="1.5rem" />;
    switch (response.reqStatus) {
      case 500:
        return "Server is not responding, please try again later.";
      case 404:
        return "The resources you are looking for can't be found. Check the URL that you were given.";
      case 200:
        switch (response.status) {
          case "PENDING":
            return "Your resources are still being processed. The page will automatically refresh when the results are ready.";
          case "DONE":
            return "Your resouces have been succesfully processed.";
          case "ERROR":
            return "There was an error when processing your files. This is most likely due to them not being valid.";
          default:
            return "Unknown error.";
        }
      default:
        return <CircularProgress size="1.5rem" />;
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Box>
      <Typography>{getMessage()}</Typography>

      {response.results && Object.entries(response.results).map(([fileName, result], i) => (
        <Typography key={i}>
          {`${fileName}: rmsd=${result.rmsd}`}
        </Typography>
      ))}

    </Box>
  );
};

export default CheckRmsd;