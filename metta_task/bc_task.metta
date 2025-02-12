;; Define cast functions between Nat and Number
(: fromNumber (-> Number Atom))
(= (fromNumber $n) (if (<= $n 0) Z (S (fromNumber (- $n 1)))))


;;chained reasoning1: if electron is in superposition it should exhibit the property of non-locality.
;;                    Electron is a quantum object, therefore it exhibits a superpositon and can be entangled.
;;chained reasoning2: if electron is measured, it's wave function will collapse. Since it was found to be
;;                    measured, it's wave function has
;;                    collapsed.


;;Knowledge Base
!(bind! &kb (new-space))

;; Electrons and photons exhibit wave-particle duality
!(add-atom &kb (Evaluation wave_particle_duality electron))
!(add-atom &kb (Evaluation wave_particle_duality photon))

;; Measurement has been performed on electron
!(add-atom &kb (Evaluation measured electron))

;; Universal truth
!(add-atom &kb (True))

;;Rule Base
!(bind! &rb (new-space))

;; if an object exhibits a Wave-particle duality,it is quantum object.
(=(wave-particle-quantum-rule) 
    (-> (Evaluation wave_particle_duality $x) 
          (Inheritance $x quantum_object)))

;; if an object is a quantum object, it exhibits superposition
(=(quantum-superposition-rule)
    (-> (Inheritance $x quantum_object)
          (Evaluation superposition $x)))

;; if an object is a quantum object, it can be entangled
(=(quantum-entanglement-rule)
    (-> (Inheritance $x quantum_object)
          (Evaluation entangled $x)))

;; if an object can be entangled, it exhibits non-locality.
(=(entanglement-nonlocality-rule)
    (-> (Evaluation entangled $x)
          (Evaluation non_local $x)))

;; if a quantum object is measured, it's wave function collapses.
(=(measurement-collapse-rule)
    (-> (Evaluation measured $x)
          (Evaluation wavefunction_collapse $x)))

!(add-reduct &rb (wave-particle-quantum-rule))
!(add-reduct &rb (quantum-superposition-rule))
!(add-reduct &rb (quantum-entanglement-rule))
!(add-reduct &rb (entanglement-nonlocality-rule))
!(add-reduct &rb (measurement-collapse-rule))

;;Backward Chainer
(: bc_bem (-> Atom Nat Atom))

;; Base case
(= (bc_bem $conclusion $depth)
   (match &kb $conclusion $conclusion))

;; Recursive case
(= (bc_bem $conclusion (S $k))
   (match &rb (-> $premise $conclusion)
          (let* (($premise (bc_bem $premise $k))) 
            $conclusion)))


!(bc_bem (Evaluation superposition electron) (fromNumber 3))
!(bc_bem (Evaluation entangled electron) (fromNumber 3))
!(bc_bem (Evaluation non_local electron) (fromNumber 3))
!(bc_bem (Evaluation wavefunction_collapse electron) (fromNumber 3))
