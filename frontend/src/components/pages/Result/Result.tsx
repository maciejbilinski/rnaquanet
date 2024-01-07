import { useEffect, useState } from "react";
import {
  Box,
  Card,
  CircularProgress,
  Fade,
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
        position: "relative",
        transition: "all 1s linear !important",
      }}
    >
      <Box
        sx={
          response?.status === "DONE"
            ? {
                ...styles.mainCard,
                flexDirection: "row",
                justifyContent: "center",
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                m: 0,
                mt: 3,
              }
            : {
                display: "flex",
                justifyContent: "center",
                mt: 3,
              }
        }
      >
        <Fade in={response?.status !== "DONE"}>
          <Stepper
            sx={{
              width: "100%",
              maxWidth: 480,
            }}
            activeStep={step.id}
            orientation="vertical"
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
                    optional="aaaa"
                    icon={loading && <CircularProgress size="1.5rem" />}
                  >
                    {stepCompleted ? s.labelFinished : s.label}
                  </StepLabel>
                  <StepContent>
                    {!step.specialDescription ? (
                      <>
                        <Typography>{s.description}</Typography>
                        <Typography fontSize="12px">
                          The page will refresh automatically.
                        </Typography>
                      </>
                    ) : (
                      <>
                        {Array.isArray(step.specialDescription) ? (
                          step.specialDescription.map((d) => (
                            <Typography>{d}</Typography>
                          ))
                        ) : (
                          <Typography>{step.specialDescription}</Typography>
                        )}
                      </>
                    )}
                  </StepContent>
                </Step>
              );
            })}
          </Stepper>
        </Fade>
      </Box>
      <Fade in={response?.status === "DONE"}>
        <Stepper activeStep={steps.length}>
          {steps.map((s, i) => (
            <Step key={i}>
              <StepLabel>{s.labelFinished}</StepLabel>
            </Step>
          ))}
        </Stepper>
      </Fade>

      {response?.files &&
        response.files.map((file, i) =>
          file.status === "SUCCESS" ? (
            <Typography key={i}>{`${file.name}: rmsd=${file.rmsd}`}</Typography>
          ) : (
            file.status === "ERROR" && (
              <Typography
                key={i}
              >{`${file.name}: Error, invalid file.`}</Typography>
            )
          )
        )}
    </Card>
  );
};

export default Result;
