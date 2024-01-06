import { useNavigate } from "react-router-dom";
import { Box, Button, Card, TextField, Typography } from "@mui/material";

import { styles } from "../../../utils/styles";
import { useState } from "react";

const TaskSearch = () => {
  const navigate = useNavigate();
  const [taskId, setTaskId] = useState<string>();
  const [error, setError] = useState<boolean>(false);

  return (
    <Card sx={styles.mainCard}>
      <Typography
        variant="h5"
        sx={{
          textAlign: "center",
        }}
      >
        Check the status of a previous task
      </Typography>

      <form
        onSubmit={(handler) => {
          handler.preventDefault();
          if (taskId) {
            navigate(`result/${taskId}`);
          } else {
            setError(true);
          }
        }}
      >
        <Box
          sx={{
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
          }}
        >
          <TextField
            sx={{ flex: 1 }}
            value={taskId ?? ""}
            onChange={(v) => {
              setError(false);
              setTaskId(v.target.value);
            }}
            InputProps={{
              sx: {
                borderTopRightRadius: { xs: "auto", md: 0 },
                borderBottomRightRadius: { xs: "auto", md: 0 },
              },
            }}
            onBlur={() => setError(false)}
            error={error}
          />
          <Button
            sx={{
              borderTopLeftRadius: { xs: "auto", md: 0 },
              borderBottomLeftRadius: { xs: "auto", md: 0 },
            }}
            type="submit"
            size="large"
            variant="contained"
            onBlur={() => setError(false)}
          >
            Search
          </Button>
        </Box>
      </form>
    </Card>
  );
};

export default TaskSearch;
