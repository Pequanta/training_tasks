;; Define cast functions between Nat and Number
(: fromNumber (-> Number Atom))
(= (fromNumber $n) (if (<= $n 0) Z (S (fromNumber (- $n 1)))))


;; fact: daul nature of both electron and photon      
;; fact2: photon is a quantum object
;; conclusion: electron is a quantum object



;Knowledge Base
!(bind! &kb (new-space))

!(add-atom &kb (Evaluation wave_particle_duality electron))
!(add-atom &kb (Evaluation wave_particle_duality photon))

;; Universal truth
!(add-atom &kb (True))



;Rule Base

!(bind! &rb (new-space))

;; if an object exhibits a Wave-particle duality,it is quantum object.
(=(wave-particle-quantum-rule) 
    (-> (Evaluation wave_particle_duality $x) 
          (Inheritance $x quantum_object)))

;; if an object is a quantum object, it exhibits superposition
(=(quantum-superposition-rule)
    (-> (Inheritance $x quantum_object)
          (Evaluation superposition $x)))

!(add-reduct &rb (wave-particle-quantum-rule))
!(add-reduct &rb (quantum-superposition-rule))

;;Forward Chainer
(= (fc $premise $depth) $premise)

;; Recursive case
(= (fc $premise1 (S $k))
   (match &rb (-> $premise1 $premise2)
          (match &kb $premise1 (fc $premise2 $k))))

!(fc (Evaluation wave_particle_duality electron) (fromNumber 2))

