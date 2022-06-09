import java.lang.System.Logger.Level;
import java.util.function.BooleanSupplier;

public class Filtro implements Semaforo{

    private int totalThreads;
    private int permits;

    volatile int[] nivel;
    volatile int[] victima;

    public Filtro(int totalThreads, int permits){
        this.totalThreads = totalThreads;
        this.permits = permits;

        nivel = new int[totalThreads];
        victima = new int[totalThreads];

        for(int i=1; i < totalThreads;++i){
            nivel[i] = 0;
        }


    }

    public boolean sameH(int i, int j) { 
        for(int k = 0; k < totalThreads; k++){
            if (k != i && nivel[k] >= j)
            return true; 
        }
        return false;
    }
    public void acquire(){
        for(int j = 1; j<totalThreads; j++){
            int ID = Integer.valueOf(Thread.currentThread().getName());

            nivel[ID] = j;
            victima[j] = ID;
            while(sameH(ID,j) && (victima[j] == ID)) ;
        }
    }

    public void release(){
        int ID = Integer.valueOf(Thread.currentThread().getName());
        nivel[ID] = 0;
    }

    @Override
    public int getPertitsOnCriticalSections() {
        // TODO Auto-generated method stub
        return 0;
    }


}