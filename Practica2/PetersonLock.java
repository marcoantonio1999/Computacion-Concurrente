/**
 * Clase que implementa el algoritmo de Peterson
 * Esta version solo funciona para 2 hilos
 */
public class PetersonLock implements Lock{
    volatile boolean[] bandera;
    volatile int victima;
    public PetersonLock(){

        this.bandera = new boolean[2];
        victima = -1;
    }

    @Override
    public void lock() {

        int ID = Integer.valueOf(Thread.currentThread().getName());
        
        bandera[ID]= true;
        victima = ID;
        while(bandera[1-ID] && victima == ID){ }
    }

    @Override
    public void unlock() {
        int ID = Integer.valueOf(Thread.currentThread().getName());
        bandera[ID]= false;
    }
    
}
