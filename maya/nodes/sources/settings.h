#ifndef SETTINGS_H
#define SETTINGS_H


#include "common.h"

enum Actication {

    kSigmoid = 0,
    kTanH,
    kSoftmax,
    kElu,
    kLeakyRelu,
    kLinear,
    k = kSigmoid

};


enum Architecture {

    kDense = 0,

};


enum Device { 

    CPU = 0,
    GPU = 1

};


class  Settings {

    public:

        Settings() :
            rate(1e-3),
            epochs(800), split(0.3),
            batchSize(32),
            shuffle(true),
            units(512),
            inputDim(100),
            layers(4),
            earlyStop(20),
            architecture(kDense),
            activation(kElu),
            device(GPU) {}
        virtual ~Settings() {}

    public:
        float           rate;
        int             epochs;
        float           split;
        int             batchSize;
        bool            shuffle;
        int             units;
        int             inputDim;
        int             layers;
        int             earlyStop;
        Architecture    architecture;
        Actication      activation;
        Device          device;

};

#endif