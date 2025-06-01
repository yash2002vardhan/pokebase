"use client";

import { useState, useRef, useEffect } from "react";
import {
  Container,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemButton,
  Alert,
  IconButton,
  Collapse,
  Box,
  Paper,
  InputAdornment,
  CircularProgress,
  Fade,
  Avatar,
  AppBar,
  Toolbar,
  Tooltip,
  Slide,
} from "@mui/material";
import { LightMode, DarkMode, Send, Terminal, CatchingPokemon } from "@mui/icons-material";
import { api } from "@/utils/api";
import Image from "next/image";

const COMMANDS = [
  "/get-pokemon-data",
  "/compare",
  "/strategy",
  "/team",
];

const pokeballUrl = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png";
const mascotUrl = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"; // Pikachu

const ALL_POKEMON = [6, 3, 9, 25, 282, 150, 448, 94, 131, 143, 196, 197, 212, 248, 330, 445, 658, 700, 809, 1, 2, 4, 7, 10, 12, 15, 18, 22, 24, 26, 38, 39, 40, 65, 68, 76, 94, 99, 112, 115, 121, 123, 130, 134, 135, 142, 149, 181, 208, 212, 214, 229, 230, 248, 254, 257, 260, 282, 302, 306, 319, 323, 334, 350, 359, 362, 373, 376, 380, 381, 384, 386, 392, 398, 405, 407, 409, 445, 448, 460, 461, 468, 472, 475, 479, 483, 485, 487, 491, 530, 534, 537, 542, 549, 553, 555, 560, 571, 609, 612, 635, 637, 642, 646, 658, 660, 681, 700, 706, 715, 719, 724, 727, 730, 740, 745, 748, 758, 760, 766, 773, 776, 778, 784, 786, 788, 800, 801, 802, 805, 809];

function getRandomFloat(min: number, max: number) {
  return Math.random() * (max - min) + min;
}

function getRandomInt(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// --- Bubble Physics Helpers ---
function distance(x1: number, y1: number, x2: number, y2: number) {
  return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
}

function resolveCollision(b1: any, b2: any, width = 1200) {
  // Simple elastic collision in 2D
  const dx = b2.x - b1.x;
  const dy = b2.y - b1.y;
  const dist = Math.sqrt(dx * dx + dy * dy) || 1;
  const nx = dx / dist;
  const ny = dy / dist;
  const p = 2 * (b1.vx * nx + b1.vy * ny - b2.vx * nx - b2.vy * ny) / 2;
  b1.vx = b1.vx - p * nx;
  b1.vy = b1.vy - p * ny;
  b2.vx = b2.vx + p * nx;
  b2.vy = b2.vy + p * ny;

  // Move bubbles apart so their boundaries just touch
  const r1 = b1.size / width * 50;
  const r2 = b2.size / width * 50;
  const overlap = r1 + r2 - dist;
  if (overlap > 0) {
    b1.x -= nx * overlap / 2;
    b1.y -= ny * overlap / 2;
    b2.x += nx * overlap / 2;
    b2.y += ny * overlap / 2;
  }
}

function getRandomizedPokemonAvatars(count = 20, width = 1200, height = 800) {
  return Array.from({ length: count }).map((_, i) => {
    const pokeId = ALL_POKEMON[getRandomInt(0, ALL_POKEMON.length - 1)];
    const direction = Math.random() > 0.5 ? 1 : -1;
    const duration = getRandomFloat(5, 12);
    const size = getRandomInt(80, 150);
    // Use x/y in vw/vh for easier collision math
    const x = getRandomFloat(10, 90);
    const y = getRandomFloat(10, 80);
    return {
      url: `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokeId}.png`,
      key: `${pokeId}-${i}-${Math.random()}`,
      direction,
      duration,
      size,
      x,
      y,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
    };
  });
}

function getRandomTarget() {
  return {
    top: getRandomFloat(5, 85),
    left: getRandomFloat(5, 85),
  };
}

function getRandomVelocity() {
  // Random velocity between -0.15 and 0.15 for both axes
  return {
    vx: (Math.random() - 0.5) * 0.3,
    vy: (Math.random() - 0.5) * 0.3,
  };
}

export default function Home() {
  const [command, setCommand] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState<number | null>(null);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const [darkMode, setDarkMode] = useState(true);
  const [cardIn, setCardIn] = useState(false);
  const [bubbles, setBubbles] = useState<any[]>([]);
  const bubblesRef = useRef<any[]>([]);
  const [mounted, setMounted] = useState(false);

  useEffect(() => { setMounted(true); }, []);

  // Animate card entrance
  useState(() => {
    setTimeout(() => setCardIn(true), 200);
  });

  // Initialize bubbles only after window is available
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const width = window.innerWidth || 1200;
      const height = window.innerHeight || 800;
      const initial = getRandomizedPokemonAvatars(20, width, height);
      setBubbles(initial);
      bubblesRef.current = initial;
    }
  }, []);

  // Physics animation
  useEffect(() => {
    if (bubbles.length === 0) return;
    let running = true;
    function animate() {
      setBubbles(prev => {
        const width = typeof window !== 'undefined' ? window.innerWidth : 1200;
        const height = typeof window !== 'undefined' ? window.innerHeight : 800;
        const newBubbles = prev.map(b => ({ ...b }));
        // Move
        for (let i = 0; i < newBubbles.length; i++) {
          let b = newBubbles[i];
          b.x += b.vx;
          b.y += b.vy;
          // Bounce off edges (vw/vh)
          const r = b.size / width * 50;
          if (b.x < 0 + r) { b.x = 0 + r; b.vx = Math.abs(b.vx); }
          if (b.x > 100 - r) { b.x = 100 - r; b.vx = -Math.abs(b.vx); }
          if (b.y < 0 + r) { b.y = 0 + r; b.vy = Math.abs(b.vy); }
          if (b.y > 100 - r) { b.y = 100 - r; b.vy = -Math.abs(b.vy); }
        }
        // Collisions
        for (let i = 0; i < newBubbles.length; i++) {
          for (let j = i + 1; j < newBubbles.length; j++) {
            const b1 = newBubbles[i];
            const b2 = newBubbles[j];
            const r1 = b1.size / width * 50;
            const r2 = b2.size / width * 50;
            const d = distance(b1.x, b1.y, b2.x, b2.y);
            if (d && d < r1 + r2) {
              resolveCollision(b1, b2, width);
            }
          }
        }
        bubblesRef.current = newBubbles;
        return newBubbles;
      });
      if (running) requestAnimationFrame(animate);
    }
    animate();
    return () => { running = false; };
  }, [bubbles.length]);

  // Filtered command suggestions
  const isTypingCommand = command.startsWith("/") && !command.includes(" ");
  const filteredSuggestions =
    isTypingCommand && command.length > 1
      ? COMMANDS.filter((c) => c.startsWith(command))
      : [];

  const handleCommand = async (e: React.FormEvent) => {
    e.preventDefault();
    setResult(null);
    setError(null);
    setLoading(true);
    setShowSuggestions(false);

    // Save to history
    setHistory((prev) => (command.trim() ? [command, ...prev.slice(0, 19)] : prev));
    setHistoryIndex(null);

    const [cmd, ...args] = command.trim().split(/\s+/);
    try {
      if (cmd === "/get-pokemon-data" && args.length === 1) {
        const res = await api.get<string>(`/pokemon/${args[0]}`);
        setResult(res);
      } else if (cmd === "/compare" && args.length === 2) {
        const res = await api.get<string>(`/pokemon/compare/${args[0]}/${args[1]}`);
        setResult(res);
      } else if (cmd === "/strategy" && args.length >= 1) {
        const query = args.join(" ");
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/pokemon/strategy`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(query),
          }
        );
        if (!res.ok) throw new Error("API call failed");
        const data = await res.json();
        setResult(data);
      } else if (cmd === "/team" && args.length >= 1) {
        const query = args.join(" ");
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/pokemon/team-building`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(query),
          }
        );
        if (!res.ok) throw new Error("API call failed");
        const data = await res.json();
        setResult(data);
      } else {
        setError("Invalid command or arguments.");
      }
    } catch (err) {
      setError("Error processing command.");
    } finally {
      setLoading(false);
    }
  };

  // Handle input changes and show suggestions
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCommand(e.target.value);
    setError(null);
    setShowSuggestions(e.target.value.startsWith("/") && !e.target.value.includes(" "));
    setHistoryIndex(null);
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: string) => {
    setCommand(suggestion + " ");
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  // Handle keyboard navigation for history and suggestions
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (showSuggestions && filteredSuggestions.length > 0) {
      if (e.key === "ArrowDown" || e.key === "Tab") {
        e.preventDefault();
        setCommand(filteredSuggestions[0] + " ");
        setShowSuggestions(false);
        return;
      }
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      if (history.length > 0) {
        const newIndex = historyIndex === null ? 0 : Math.min(historyIndex + 1, history.length - 1);
        setHistoryIndex(newIndex);
        setCommand(history[newIndex]);
      }
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      if (history.length > 0) {
        if (historyIndex === null) return;
        if (historyIndex === 0) {
          setHistoryIndex(null);
          setCommand("");
        } else {
          setHistoryIndex(historyIndex - 1);
          setCommand(history[historyIndex - 1]);
        }
      }
    }
  };

  // Toggle dark/light mode (optional, since MUI theme is dark by default)
  const handleToggleDarkMode = () => {
    setDarkMode((prev) => !prev);
    // In a real app, you would update the theme provider here
  };

  if (!mounted) return null;

  return (
    <Box sx={{ minHeight: "100vh", width: "100vw", position: "relative", overflow: "hidden", display: 'flex', flexDirection: 'column' }}>
      {/* Playful Pokémon accent circles */}
      <div className="poke-bg-circle poke-bg1" />
      <div className="poke-bg-circle poke-bg2" />
      <div className="poke-bg-circle poke-bg3" />
      <div className="poke-bg-circle poke-bg4" />
      {/* Randomized Interactive Floating Pokémon Bubbles */}
      {bubbles.map((bubble, i) => (
        <div
          key={bubble.key}
          style={{
            position: "absolute",
            zIndex: 3,
            left: typeof window !== 'undefined' ? `calc(${bubble.x}vw - ${bubble.size / 2}px)` : 0,
            top: typeof window !== 'undefined' ? `calc(${bubble.y}vh - ${bubble.size / 2}px)` : 0,
            width: bubble.size,
            height: bubble.size,
            pointerEvents: 'auto',
            transition: 'none',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
          onMouseEnter={() => {
            setBubbles(prev => prev.map((b, idx) => idx === i ? { ...b, vx: -b.vx + (Math.random() - 0.5) * 0.16, vy: -b.vy + (Math.random() - 0.5) * 0.16 } : b));
          }}
          onClick={() => {
            setBubbles(prev => prev.map((b, idx) => idx === i ? { ...b, vx: -b.vx + (Math.random() - 0.5) * 0.16, vy: -b.vy + (Math.random() - 0.5) * 0.16 } : b));
          }}
        >
          <div
            style={{
              width: bubble.size,
              height: bubble.size,
              borderRadius: '50%',
              background: 'rgba(255,255,255,0.13)',
              boxShadow: '0 4px 24px 0 rgba(0,0,0,0.10)',
              border: '2.5px solid rgba(255,255,255,0.35)',
              backdropFilter: 'blur(8px) saturate(180%)',
              WebkitBackdropFilter: 'blur(8px) saturate(180%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              overflow: 'hidden',
            }}
          >
            <Avatar
              src={bubble.url}
              alt="pokemon"
              sx={{
                width: '80%',
                height: '80%',
                opacity: 0.95,
                background: 'none',
                boxShadow: 0,
                border: 0,
                filter: 'drop-shadow(0 2px 8px rgba(0,0,0,0.10))',
              }}
            />
          </div>
        </div>
      ))}
      <style jsx global>{`
        ${Array.from({ length: 20 })
          .map(
            (_, i) =>
              `@keyframes float${i} { 0% { transform: translateY(0); } 100% { transform: translateY(${getRandomInt(-30, 30)}px); } }`
          )
          .join('\n')}
        @keyframes bubbleIn {
          from { transform: scale(0.8) translateY(30px); opacity: 0; }
          to { transform: scale(1) translateY(0); opacity: 1; }
        }
      `}</style>
      {/* Main Command UI - Glassmorphism Box */}
      <Box
        sx={{
          flex: 1,
          width: '100vw',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 10,
          px: 2,
          py: 4,
        }}
      >
        <Box
          sx={{
            width: { xs: '100%', sm: 600 },
            maxWidth: '98vw',
            bgcolor: 'rgba(24, 28, 36, 0.85)',
            borderRadius: 12,
            boxShadow: 12,
            backdropFilter: 'blur(16px) saturate(160%)',
            WebkitBackdropFilter: 'blur(16px) saturate(160%)',
            border: '1.5px solid #fff',
            p: { xs: 2, sm: 4 },
            mx: 'auto',
            my: 2,
            zIndex: 20,
            position: 'relative',
          }}
        >
          {/* Main content starts here */}
          <Typography sx={{ color: '#fff' }} mb={1} fontSize={{ xs: 18, md: 22 }} fontWeight={700}>
            Use slash commands to interact with Pokebase:
          </Typography>
          <List dense sx={{ color: "#fff", mb: 2, width: '100%' }}>
            <ListItem>
              <Typography component="span" sx={{ color: '#ffcb05', fontWeight: 700, fontSize: 18 }}>/get-pokemon-data &lt;name&gt;</Typography> <span style={{color:'#eee'}}>— Get Pokémon description</span>
            </ListItem>
            <ListItem>
              <Typography component="span" sx={{ color: '#ffcb05', fontWeight: 700, fontSize: 18 }}>/compare &lt;name1&gt; &lt;name2&gt;</Typography> <span style={{color:'#eee'}}>— Compare two Pokémon</span>
            </ListItem>
            <ListItem>
              <Typography component="span" sx={{ color: '#ffcb05', fontWeight: 700, fontSize: 18 }}>/strategy &lt;query&gt;</Typography> <span style={{color:'#eee'}}>— Get strategy suggestion</span>
            </ListItem>
            <ListItem>
              <Typography component="span" sx={{ color: '#ffcb05', fontWeight: 700, fontSize: 18 }}>/team &lt;query&gt;</Typography> <span style={{color:'#eee'}}>— Get team suggestion</span>
            </ListItem>
          </List>
          <Box component="form" onSubmit={handleCommand} sx={{ position: "relative", width: '100%' }}>
            <TextField
              inputRef={inputRef}
              fullWidth
              variant="outlined"
              size="medium"
              label="Command"
              placeholder="Type a command, e.g. /get-pokemon-data pikachu"
              value={command}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              error={!!error}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Terminal fontSize="small" sx={{ color: '#fff' }} />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton type="submit" sx={{ color: '#fff', transition: 'background 0.2s', '&:hover': { background: '#fffde7', color: '#222' } }} disabled={loading} edge="end">
                      {loading ? <CircularProgress size={22} color="inherit" /> : <Send />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              sx={{ mb: 1, bgcolor: "#181c24", color: '#fff', input: { color: '#fff' }, label: { color: '#fff' } }}
              autoFocus
              autoComplete="off"
            />
            <Collapse in={showSuggestions && filteredSuggestions.length > 0}>
              <Paper elevation={3} sx={{ position: "absolute", left: 0, right: 0, zIndex: 10, mt: 0.5, borderRadius: 2 }}>
                <List dense>
                  {filteredSuggestions.map((s) => (
                    <ListItem key={s} disablePadding>
                      <ListItemButton
                        onClick={() => handleSuggestionClick(s)}
                        sx={{ cursor: "pointer", px: 2, py: 1, color: '#ffcb05', '&:hover': { bgcolor: "#ffcb05", color: "#222" } }}
                      >
                        {s}
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Collapse>
            {error && (
              <Alert severity="error" sx={{ mt: 2, borderRadius: 2 }}>
                {error}
              </Alert>
            )}
          </Box>
          <Button
            type="submit"
            variant="contained"
            sx={{ mt: 2, fontWeight: 700, fontSize: 18, boxShadow: 3, letterSpacing: 1, borderRadius: 3, transition: 'background 0.2s', width: '100%', background: '#ffcb05', color: '#222', '&:hover': { background: '#ffe066', color: '#222' } }}
            onClick={handleCommand}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : "RUN COMMAND"}
          </Button>
          {result && (
            <Box sx={{ mt: 3, display: 'flex', width: '100%', mx: 'auto', justifyContent: 'center' }}>
              <Paper sx={{ p: 2, borderRadius: 3, bgcolor: "#23272f", maxWidth: '90%', boxShadow: 4, border: '1.5px solid #1976d2', position: 'relative', animation: 'bubbleIn 0.5s' }}>
                <Typography variant="body2" fontFamily="monospace" whiteSpace="pre-wrap" color="#fff">
                  {result}
                </Typography>
                <Box sx={{ position: 'absolute', right: -16, top: 16 }}>
                  <Avatar src={mascotUrl} alt="Pikachu" sx={{ width: 32, height: 32, bgcolor: 'transparent' }} />
                </Box>
              </Paper>
            </Box>
          )}
        </Box>
      </Box>
    </Box>
  );
}
