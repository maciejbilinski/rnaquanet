import { useEffect, useState } from "react";
import {
  Box,
  Card,
  CircularProgress,
  Step,
  StepContent,
  StepLabel,
  Stepper,
  Typography,
} from "@mui/material";

import { API_ADDRESS, REQUEST_RETRY_DELAY } from "../../../../config";
import { styles } from "../../../utils/styles";
import { steps, getCurrentStep } from "./steps";

const Result = () => {
  const [response, setResponse] = useState<TaskResult>();
  const [currentStep, setCurrentStep] = useState<Step>({ id: 0, status: "loading" });

  const fetchData = async () => {
    try {
      const task_id = location.pathname.split("/").pop();
      const res = await fetch(`${API_ADDRESS}/check_rmsd/${task_id}`, {
        method: "GET",
      });

      // parse received data
      const json: TaskResult = {
        status_code: res.status,
        ...(await res.json()),
      };
      console.log(json);
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
    setCurrentStep(getCurrentStep(response));
  }, [response]);

  return (
    <Card sx={styles.mainCard}>
      <Stepper activeStep={currentStep.id} orientation="vertical">
        {steps.map((step, i) => (
          <Step key={i}>
            <StepLabel>{step.label}</StepLabel>
            <StepContent>
              <Typography>{step.description}</Typography>
              {response?.status && response.status !== "DONE" && (
                <Typography fontSize="12px">
                  The page will refresh automatically.
                </Typography>
              )}
            </StepContent>
          </Step>
        ))}
      </Stepper>

      {response?.files &&
        response.files.map((file, i) =>
          file.status === "SUCCESS" ? (
            <Typography key={i}>{`${file.name}: rmsd=${file.rmsd}`}</Typography>
          ) : (
            <Typography
              key={i}
            >{`${file.name}: Error, invalid file.`}</Typography>
          )
        )}
    </Card>
  );
};

export default Result;
