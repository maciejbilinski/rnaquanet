import { Card, Typography } from "@mui/material";

import { styles } from "../../../utils/styles";
import { projectName } from "../../../../config";

const ProjectInfo = () => {
  return (
    <Card
      sx={{
        ...styles.mainCard,
        py: 6,
      }}
    >
      <Typography>
        {projectName} is an application performing quality assessment on RNA
        structures. It reads your uploaded files and processes them using our
        model trained using neural networks to generate an RMSD score.
        <br />
        After you submit your task, simply save the generated url to see your
        results later on.
        <br />
        This website is free and open to all users and there is no login
        requirement.
      </Typography>
    </Card>
  );
};

export default ProjectInfo;
