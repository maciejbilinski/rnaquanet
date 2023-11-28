import { Dispatch, SetStateAction } from "react";
import { Box, Button, Card, Typography } from "@mui/material";

import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { styles } from "../utils/styles";
import { PROJECT_NAME } from "../../config";

interface NavbarProps {
  colorMode: string;
  setColorMode: Dispatch<SetStateAction<"light" | "dark">>;
}

const Navbar = ({
  colorMode,
  setColorMode,
}: NavbarProps) => {
  return (
    <Card sx={{
      ...styles.mainCard,
      flexDirection: "row",
      justifyContent: "space-between",
      alignItems: "center",
    }}>
      {/* filler box */}
      <Box sx={{
        flex: 1
      }} />

      {/* project name */}
      <Box sx={{
        flex: 1,
        display: "flex",
        justifyContent: "center",
      }}>
        <Typography variant="h4" sx={{ fontFamily: "initial" }}>
          {PROJECT_NAME}
        </Typography>
      </Box>

      {/* theme toggle button */}
      <Box sx={{
        flex: 1,
        display: "flex",
        justifyContent: "flex-end",
      }}>
        <Button
          onClick={() => setColorMode(colorMode === "dark" ? "light" : "dark")}
        >
          {colorMode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
        </Button>
      </Box>
    </Card>
  );
};

export default Navbar;