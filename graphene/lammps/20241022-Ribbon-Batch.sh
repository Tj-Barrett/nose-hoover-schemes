
declare -a tls=(21 22 23 24 25 26 27 28 29 30 31 32)

for tl in "${tls[@]}"; do
	mpirun -np 12 lmp -in 20241022_Graphene-Tensile-NVT-Ribbon.in -v tensile_loop ${tl}
done 

for tl in "${tls[@]}"; do
	mpirun -np 12 lmp -in 20241022_Graphene-Tensile-NPT-Ribbon.in -v tensile_loop ${tl} -v pdamp 1000
done 