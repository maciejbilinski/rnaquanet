import { useEffect, useState } from "react";
import { Box, Card, CircularProgress, Typography } from "@mui/material";

import { API_ADDRESS, REQUEST_RETRY_DELAY } from "../../../../config";
import { styles } from "../../../utils/styles";

const Result = () => {
  const [response, setResponse] = useState<ITaskResultRes>({});

  const fetchData = async () => {
    try {
      const res = await fetch(
        `${API_ADDRESS}/check_rmsd/${location.pathname.split("/").pop()}`,
        {
          method: "GET",
        }
      );

      // if the API responded correctly, parse received data
      let json: TaskResultRes = {};
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
    } catch (error) {
      setResponse({
        reqStatus: 500,
      });
      console.error(error);
      setTimeout(fetchData, REQUEST_RETRY_DELAY);
    }
  };

  const getMessage = () => {
    switch (response.reqStatus) {
      case 500:
        return "Server is not responding, please try again later.";
      case 404:
        return "The resources you are looking for can't be found. Check the URL that you were given.";
      case 200:
        switch (response.status) {
          case "PENDING":
            return (
              <>
                <Box>
                  <Typography>Your files are being processed.</Typography>
                  <Typography>
                    The page will automatically refresh when the results are
                    ready.
                  </Typography>
                </Box>
                <CircularProgress size="1.5rem" />
              </>
            );
          case "DONE":
            return "Your files have been succesfully processed.";
          case "ERROR":
            return "There was an error when processing your files. This is most likely due to them being invalid.";
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
    <Card sx={styles.mainCard}>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          gap: 2,
        }}
      >
        {getMessage()}
      </Box>

      {response.results &&
        Object.entries(response.results).map(([fileName, result], i) => (
          <Typography key={i}>{`${fileName}: rmsd=${result.rmsd}`}</Typography>
        ))}
    </Card>
  );
};

export default Result;
