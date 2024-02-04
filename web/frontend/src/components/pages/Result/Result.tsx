import { useEffect, useState } from "react";
import {
  Box,
  Card,
  CircularProgress,
  Step,
  StepLabel,
  Stepper,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";

import { API_ADDRESS, REQUEST_RETRY_DELAY } from "../../../../config";
import { styles } from "../../../utils/styles";
import { steps, getCurrentStep } from "./steps";

const Result = () => {
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("md"));
  const [response, setResponse] = useState<TaskResult>();
  const [step, setStep] = useState<Step>({
    id: 0,
    status: "loading",
  });

  const fetchData = async () => {
    try {
      const task_id = location.pathname.split("/").pop();
      const res = await fetch(`${API_ADDRESS}/check_rmsd/${task_id}`, {
        method: "GET",
      });

      // parse received data
      const json: TaskResult = {
        status_code: res.status,
        ...(res.status === 200 ? await res.json() : {}),
      };
      setResponse(json);

      // if file has not yet finished processing and there were no errors
      // set a simeout to check again in `REQUEST_RETRY_DELAY` ms
      if (
        json.status_code === 200 &&
        json.status !== "DONE" &&
        json.status !== "ERROR"
      ) {
        setTimeout(fetchData, REQUEST_RETRY_DELAY);
      }
    } catch (error) {
      setResponse({ status_code: 500 });
      setTimeout(fetchData, REQUEST_RETRY_DELAY);
    }
  };

  useEffect(() => {
    setTimeout(fetchData, 1000);
  }, []);

  useEffect(() => {
    setStep(getCurrentStep(step.id, response));
  }, [response]);

  return (
    <Card
      sx={{
        ...styles.mainCard,
        minHeight: 640,
      }}
    >
      <Stepper
        activeStep={step.id}
        orientation={isSmallScreen ? "vertical" : "horizontal"}
      >
        {steps.map((s, i) => {
          const cur = step.id === i;
          const failed = cur && step.status === "failed";
          const loading = cur && step.status === "loading";
          const stepCompleted = step.id > i;

          return (
            <Step key={i}>
              <StepLabel
                error={failed}
                icon={loading && <CircularProgress size="1.5rem" />}
                optional={
                  cur && (
                    <Typography fontSize="12px">
                      {step.specialDescription ??
                        "Page will refresh automatically"}
                    </Typography>
                  )
                }
              >
                {stepCompleted ? s.labelFinished : s.label}
              </StepLabel>
            </Step>
          );
        })}
      </Stepper>

      {response?.status === "DONE" && response.files && (
        <Box
          sx={{
            mt: 5,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <table style={{ width: "100%", maxWidth: 500 }}>
            <thead>
              <tr>
                <th style={{ padding: "5px 2px" }}>File name</th>
                <th style={{ padding: "5px 2px" }}>Model</th>
                <th style={{ padding: "5px 2px" }}>Chain</th>
                <th style={{ padding: "5px 2px" }}>RMSD</th>
              </tr>
            </thead>
            <tbody>
              {response.files.map((file, i) => (
                <tr key={i}>
                  <td style={{ padding: "5px 10px" }}>{file.name}</td>
                  <td style={{ padding: "5px 10px" }}>{file.selectedModel + 1}</td>
                  <td style={{ padding: "5px 10px" }}>{file.selectedChain}</td>
                  <td
                    style={{
                      padding: "5px 10px",
                      textAlign: file.status === "SUCCESS" ? "right" : "center",
                    }}
                  >
                    {file.status === "SUCCESS"
                      ? file.rmsd?.toFixed(4)
                      : "Invalid file!"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Box>
      )}
    </Card>
  );
};

export default Result;
