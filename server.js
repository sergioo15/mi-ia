const express = require('express');
const app = express();

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ mensaje: "IA funcionando" });
});

app.post('/api/chat', (req, res) => {
  const mensaje = req.body.message;
  const respuestaIA = `IA responde a: ${mensaje}`;
  res.json({ response: respuestaIA });
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Servidor IA corriendo");
});

