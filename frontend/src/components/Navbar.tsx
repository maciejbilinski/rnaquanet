import { Dispatch, SetStateAction } from "react";
import { Button, Card } from "@mui/material";

import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import { styles } from "../utils/styles";

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
      justifyContent: "flex-end",
    }}>
      {/* theme toggle button */}
      <Button
        onClick={() => setColorMode(colorMode === "dark" ? "light" : "dark")}
      >
        {colorMode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
      </Button>
    </Card>
  );
};

export default Navbar;