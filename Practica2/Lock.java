/**
 * Interfaz para crear un candado que cumpla con exclusion mutua
 */
public interface Lock{

    /**
     * El hilo actual adquiere el candado. Esperara x cantidad de tiempo antes de que otro hilo lo tome
     */
    public void lock();

    /**
     * El hilo actual deja el candado. Esto servira para que otro Hilo lo adquiera
     */
    public void unlock();
}