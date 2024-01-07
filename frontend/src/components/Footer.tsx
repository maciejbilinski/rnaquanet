import { Box, Link, Typography } from "@mui/material";

import { projectName, repositoryLink } from "../../config";

const Footer = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        p: 3,
      }}
    >
      <Link href={repositoryLink} target="_blank">
        Learn more about the project
      </Link>
      <Typography>
        {projectName} 2024 | Poznan University of Technology
      </Typography>
    </Box>
  );
};

export default Footer;
