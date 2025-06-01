"use client";
import { ThemeProvider, CssBaseline } from "@mui/material";
import theme from "./mui-theme";

export default function MuiProvider({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
} 
