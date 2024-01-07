import { Dispatch, SetStateAction } from "react";
import { Box, Button, Card, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import LightModeIcon from "@mui/icons-material/LightMode";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import { styles } from "../utils/styles";
import { projectName } from "../../config";

interface Props {
  colorMode: string;
  setColorMode: Dispatch<SetStateAction<"light" | "dark">>;
}

const Navbar = ({ colorMode, setColorMode }: Props) => {
  return (
    <Card
      sx={{
        ...styles.mainCard,
        bgcolor: "primary.main",
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        p: 1,
      }}
    >
      {/* filler box */}
      <Box sx={{ flex: 1 }} />

      {/* project name */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Link
          to={window.origin}
          style={{
            textDecoration: "none",
            color: "#fff",
          }}
        >
          <Typography variant="h4" sx={{ fontFamily: "initial" }}>
            {projectName}
          </Typography>
        </Link>
      </Box>

      {/* theme toggle button */}
      <Box
        sx={{
          flex: 1,
          display: "flex",
          justifyContent: "flex-end",
        }}
      >
        <Button
          size="large"
          sx={{ color: "#fff" }}
          onClick={() => setColorMode(colorMode === "light" ? "dark" : "light")}
        >
          {colorMode === "light" ? <LightModeIcon /> : <DarkModeIcon />}
        </Button>
      </Box>
    </Card>
  );
};

export default Navbar;
