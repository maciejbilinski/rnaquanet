import { useState } from "react";
import { Card, Divider, Typography } from "@mui/material";

import { styles } from "../../../utils/styles";

import UploaderDataBank from "./UploaderDataBank";
import UploaderUserFile from "./UploaderUserFile";
import RequestButton from "./RequestButton";

const Main = () => {
  const [files, setFiles] = useState<FileData[]>([]);

  return (
    <Card
      sx={{
        ...styles.mainCard,
        py: 4,
        gap: 4,
      }}
    >
      <Typography
        variant="h5"
        sx={{
          textAlign: "center",
          mb: 2,
        }}
      >
        Upload RNA structures
      </Typography>
      <UploaderDataBank files={files} setFiles={setFiles} />
      <Divider variant="middle" />
      <UploaderUserFile files={files} setFiles={setFiles} />
      <Divider variant="middle" />
      <RequestButton files={files} setFiles={setFiles} />
    </Card>
  );
};

export default Main;
