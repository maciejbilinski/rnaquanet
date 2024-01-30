import { useEffect, useState } from "react";
import {
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
