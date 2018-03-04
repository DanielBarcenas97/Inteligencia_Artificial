package ia;

import processing.core.PApplet;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;

import java.util.List;
import java.util.Random;
import java.util.Stack;

/**
 *
 * @author Ángel Gladín
 */
public class Maze extends PApplet {

    /// Hola ayudante o persona que me va a calificar la práctica, estas
    /// constantes las puedas probar con diferentes tamaños.
    final int CELL_HEIGHT = 15;
    final int CELL_WIDTH = 15;
    final int CELL_SIZE = 30;

    final float fpsRefreshRate = 60f;

    Random random = new Random();

    MazeGenerator mazeGenerator;

    @Override public void setup() {
        frameRate(fpsRefreshRate);

        size(CELL_WIDTH * CELL_SIZE, CELL_HEIGHT * CELL_SIZE);

        // Crear los cuadros que no tendrán nada.
        for (int i = 0; i < CELL_HEIGHT; i++) {
            for (int j = 0; j < CELL_WIDTH; j++) {
                // Agregar al canvas un cuadro gris con bordes negros.
                stroke(0);
                fill(128, 128, 128);
                rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE);
            }
        }

        // Obtenemos una posición aleatoria de la celda inicial.
        int x = random.nextInt(CELL_WIDTH);
        int y = random.nextInt(CELL_HEIGHT);

        // Cuadro inicial, se pondrá de color rosa.
        fill(255, 61, 127);
        rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE);

        // Incializamos el laberinto con una celda que es la que se
        // agregó aleatoriamente.
        this.mazeGenerator = new MazeGenerator(new Cell(x, y, -1), CELL_WIDTH, CELL_HEIGHT);
    }


    /**
     * Método que se manda a llamar cada vez que se dibuja en el canvas.
     */
    @Override public void draw() {

        mazeGenerator.yieldPath((x, y, direction, cellType) -> {
            // Fijarnos en que tipo de celda es, esto es para colorear difernte.
            if (cellType == CellType.CURRENT) {

                // La nueva celda explorada (azul y sin borde).
                fill(29, 202, 214);
                noStroke();
                rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1);

                // La líneas que se pintará será azul.
                stroke(29, 202, 214);
                // Se dibuja una línea porque es como si quitaramos una pared.
                switch (direction) {
                case MazeGenerator.N:
                    line (x * CELL_SIZE + 1, y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + CELL_SIZE - 1, y * CELL_SIZE + CELL_SIZE);
                    break;
                case MazeGenerator.S:
                    line (x * CELL_SIZE + 1, y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE - 1, y * CELL_SIZE);
                    break;
                case MazeGenerator.E:
                    line(x * CELL_SIZE, y * CELL_SIZE + 1, x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE - 1);
                    break;
                case MazeGenerator.W:
                    line (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + 1, x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE - 1);
                    break;
                default:
                    break;
                }
            } else {
                noStroke();
                fill(255, 61, 127);
                rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1);

                // La líneas que se pintará será rosa.
                stroke(255, 61, 127);
                // Se dibuja una línea porque es como si quitaramos una pared.
                switch (direction) {
                case MazeGenerator.N:
                    line (x * CELL_SIZE + 1, y * CELL_SIZE + CELL_SIZE, x * CELL_SIZE + CELL_SIZE - 1, y * CELL_SIZE + CELL_SIZE);
                    break;
                case MazeGenerator.S:
                    line (x * CELL_SIZE + 1, y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE - 1, y * CELL_SIZE);
                    break;
                case MazeGenerator.E:
                    line(x * CELL_SIZE, y * CELL_SIZE + 1, x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE - 1);
                    break;
                case MazeGenerator.W:
                    line (x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + 1, x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE - 1);
                    break;
                default:
                    break;
                }

            }
        });

    }


    /**
     * Representación de una celda.
     */
    class Cell {
        int x, y, direction;

        Cell(int x, int y, int direction) {
            this.x = x;
            this.y = y;
            this.direction = direction;
        }
    }

    /**
     * Generador de laberintos. Me base mucho en
     * <a href="http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking">
     * esta página</a>.
     */
    class MazeGenerator {
        // Indicadores de dirección.
        static final int N = 1, S = 2, E = 3, W = 4;

        int[][] grid;
        int gridWidth, gridHeight;
        int grids;

        // Auxiliares para mapear direcciones
        HashMap<Integer, Integer> dx = new HashMap<>();
        HashMap<Integer, Integer> dy = new HashMap<>();
        HashMap<Integer, Integer> opposite = new HashMap<>();

        Stack<Cell> cellStackPath = new Stack<>();
        Stack<Cell> auxStackPath = new Stack<>();

        Cell firstCell;

        MazeGenerator(Cell cell, int gridWidth, int gridHeight) {
            this.gridWidth = gridWidth;
            this.gridHeight = gridHeight;

            this.grids = gridWidth * gridHeight;

            this.grid = new int [gridWidth][gridHeight];

            dx.put(E, 1);    dx.put(W, -1);    dx.put(N, 0);    dx.put(S, 0);
            dy.put(E, 0);    dy.put(W, 0);     dy.put(N, -1);   dy.put(S, 1);

            opposite.put(E, W);   opposite.put(W, E);
            opposite.put(N, S);   opposite.put(S, N);

            cellStackPath.push(cell);

            firstCell = cell;
        }

        /**
         * Generador de caminos del laberinto por cada vez que sea llamado.
         * Se implenetó así para que cada determinado tiempo que se esté
         * llamando vaya generando un camino.
         * @param cellPainter Una "función" que tendrá de parámetros que
         *                    tipo de celda es, dirección y sus coordenadas.
         */
        void yieldPath(CellPainter cellPainter) {
            if (!cellStackPath.empty()) {
                List<Integer> directions = Arrays.asList(N, S, E, W);
                Collections.shuffle(directions);
                Cell cellAux = cellStackPath.pop();

                for (Integer dir : directions) {
                    int nx = cellAux.x + dx.get(dir);
                    int ny = cellAux.y + dy.get(dir);

                    if (nx >= 0 && nx < gridWidth && ny >= 0 && ny < gridHeight &&
                            grid[nx][ny] == 0) {
                        grid[cellAux.x][cellAux.y] = dir;
                        grid[nx][ny] = opposite.get(dir);

                        cellStackPath.push(new Cell(nx, ny, dir));
                        auxStackPath.push(new Cell(nx, ny, dir));

                        cellPainter.action(nx, ny, dir, CellType.CURRENT);

                        break;
                    }
                }
            } else if (!auxStackPath.empty()) {
                Cell aux = auxStackPath.pop();
                // Aquí es donde enseñamos explícitamente el backtracking.
                cellPainter.action(aux.x, aux.y, aux.direction, CellType.VISITED);
                cellStackPath.push(aux); 
            } else if (cellStackPath.empty()) {
                // La celda con la que empezamos, al final de crear el laberinto
                // la volvemos a colorear.
                cellPainter.action(firstCell.x, firstCell.y, firstCell.direction, CellType.VISITED);
            } 
        }

    }

    /**
     * Indicador de que tipo de celda es. Se utilizó para de acuerdo el tipo ver
     * como se hace el backtrack.
     */
    enum CellType { CURRENT, VISITED }

    /**
     * Interfaz funcional que se usará para ir pintando el canvas.
     * <p>
     * Tenemos que hacer esto para poder pasar una función como parámetro porque
     * Java apesta por no tener funciones orden superior.
     * @param x         [La cordenada x de la celda]
     * @param y         [La cordenada y de la celda]
     * @param direction [La dirección de donde "ve" la celda]
     * @param cellType  [description]
     */
    @FunctionalInterface interface CellPainter {
        void action(int x, int y, int direction, CellType cellType);
    }

    static public void main(String args[]) {
        PApplet.main(new String[] {"ia.Maze"});
    }
}
