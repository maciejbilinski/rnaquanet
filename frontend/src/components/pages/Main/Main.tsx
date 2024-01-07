import { useState } from "react";
import { Card, Divider, Typography } from "@mui/material";

import { styles } from "../../../utils/styles";

import ProjectInfo from "../ProjectInfo/ProjectInfo";
import UploaderDataBank from "./UploaderDataBank";
import UploaderUserFile from "./UploaderUserFile";
import RequestButton from "./RequestButton";
import TaskSearch from "../TaskSearch/TaskSearch";

const Main = () => {
  const [files, setFiles] = useState<FileData[]>([]);

  return (
    <>
      <ProjectInfo />
      <Card sx={styles.mainCard}>
        <Typography
          variant="h5"
          sx={{
            textAlign: "center",
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
      <TaskSearch />
    </>
  );
};

export default Main;
