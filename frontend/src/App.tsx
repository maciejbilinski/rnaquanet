import { useEffect, useMemo } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useLocalStorage } from "usehooks-ts";
import { Box } from "@mui/material";

import Navbar from "./components/Navbar";
import Main from "./components/pages/Main/Main";
import Footer from "./components/Footer";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { projectName } from "../config";
import TaskSearch from "./components/pages/TaskSearch/TaskSearch";
import TaskResult from "./components/pages/TaskResult/TaskResult";

const App = () => {
  const [colorMode, setColorMode] = useLocalStorage<"light" | "dark">(
    "ColorMode",
    "light"
  );

  useEffect(() => {
    document.title = projectName;
  }, []);

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: colorMode,
          background: {
            default: colorMode === "light" ? "#dbdbdb" : "#121212",
            paper: colorMode === "light" ? "#f9f9f9" : undefined,
          },
          primary: {
            main: "#3ca93c",
          },
          secondary: {
            main: "#194519",
          },
        },
        breakpoints: {
          values: {
            xs: 0,
            sm: 600,
            md: 900,
            lg: 1200,
            xl: 1536,
          },
        },
      }),
    [colorMode]
  );

  return (
    <BrowserRouter>
      <ThemeProvider theme={theme}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            bgcolor: "background.default",
            color: "text.primary",
            minHeight: "100dvh",
            gap: 1.5,
          }}
        >
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              width: "100%",
              maxWidth: 1200,
              gap: 1.5,
              mt: 0.5,
            }}
          >
            <Navbar colorMode={colorMode} setColorMode={setColorMode} />

            <Routes>
              <Route
                path="/"
                element={<Main />}
              />
              <Route path="/result" element={<TaskSearch />} />
              <Route path="/result/*" element={<TaskResult />} />
            </Routes>
          </Box>
          <Footer />
        </Box>
      </ThemeProvider>
    </BrowserRouter>
  );
};

export default App;
