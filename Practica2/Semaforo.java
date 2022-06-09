public interface Semaforo {
    
    /**
     * Metodo que nos regresa el numero de permitidos en la CS
     * @return El numero de permitidos
     */
    public int getPertitsOnCriticalSections();

    /**
     * Para que un hilo tome el candado
     */
    public void acquire();

    /**
     * Para que un hilo lo libere
     */
    public void release();
}
