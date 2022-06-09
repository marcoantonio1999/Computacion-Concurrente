public class PetersonLockTest {
    static final int ITERATIONS = 100;
    static final int MAX_VALUE = 50000;
    static int APROVATION = 0;
    Lock lock;
    Counter counter;


    void lock() throws InterruptedException {
        Thread[] threads = new Thread[2];
        for(int i = 0; i < ITERATIONS; i++) {
            counter = new Counter();
            threads[0] = new Thread(this::incrementCounter, "0");
            threads[1] = new Thread(this::incrementCounter, "1");
            threads[0].start();
            threads[1].start();

            threads[0].join();
            threads[1].join();

            assertEquals(2 * MAX_VALUE, counter.getValue());
        }
        if(APROVATION > 65){
            System.out.println("Prueba superada \nAprovacion del: "+ APROVATION+"%");
        }
    }

    void incrementCounter() {
        for(int i = 0; i < MAX_VALUE; i++) {
            counter.getAndIncrement();
        }
    }

    void assertEquals(int value, int expected){
        if(value != expected){
            System.out.println("Los valores no concuerdan");
        }else{
            ++APROVATION;
        }
    }

    public static void main(String[] args) throws InterruptedException{
        PetersonLockTest plt = new PetersonLockTest();
        plt.lock();
    }
}

class Counter {
    private volatile int value;
    private Lock lock;

    Counter() {
        this.value = 0;
        this.lock = new PetersonLock();
    }
    int getAndIncrement() {
        this.lock.lock();
        int result = this.value;
        this.value = this.value + 1;
        this.lock.unlock();
        return result;
    }

    int getValue() {
        return value;
    }
}