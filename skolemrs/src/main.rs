extern crate permutohedron;
use std::thread;

use std::time::Instant;

#[allow(unused_macros)]
macro_rules! mt_skolem_dual_head_tail {
    ($k:expr) => {
        {
            fn skolem_check_no_alloc_min_shift(head1: u8, head2: u8, ordering: [u8; $k - 3], tail: u8) -> bool {
                let (mut skolem, mut iters_so_far): (u64, u8) = if head1 == 1 {
                    (1 << (head2 - 1), 3)
                } else {
                    ((1 << (head1 - 2)) | (1 << (head2-1)), 2)
                };

                for &i in &ordering {
                    let x = skolem.trailing_ones() as u8;
                    skolem >>= x;

                    if (skolem & (1 << i)) != 0 {
                        return false;
                    }

                    iters_so_far += x + 1;
                    if iters_so_far > 2 * $k - i {
                        return false;
                    }

                    skolem |= 1 << i;
                    skolem >>= 1;
                }

                let x = skolem.trailing_ones() as u8;
                skolem >>= x;

                if (skolem & (1 << tail)) != 0 {
                    return false;
                }

                iters_so_far + x + 1 <= 2 * $k - tail
            }

            fn check_skolem_head_tail(head1: u8, head2: u8, body: &[u8; $k - 3], tail: u8) -> usize {
                let max_valid = ($k * 2 + 2) / 3;

                if head1 - 1 == head2 || tail > max_valid {
                    return 0;
                }

                let mut x = 0;

                let mut body = body.clone();

                for body in permutohedron::Heap::new(&mut body) {
                    if skolem_check_no_alloc_min_shift(head1, head2, body, tail) {
                        x += 1;
                    }
                }

                x
            }

            fn check_all_skolem() -> usize {
                if $k == 0 {
                    return 0;
                } else if $k == 1 {
                    return 1;
                } else if [2, 3].contains(&($k % 4)) {
                    return 0;
                }

                let max_valid = ($k * 2 + 2) / 3;

                let handlers: Vec<_> = (1u8..=$k).into_iter().map(|head1| {
                    let subhandlers: Vec<_> = (1u8..=$k)
                        .filter(|&x| x != head1 && x != head1 - 1)
                        .map(|head2| {
                            let subsubhandlers: Vec<_> = (1u8..=$k)
                                .filter(|&x| x != head1 && x != head2 && x <= max_valid)
                                .map(|tail| {
                                    let vbody: Vec<u8> = (1u8..=$k).filter(|&j| j != head1 && j != head2 && j != tail).collect();
                                    let mut body = [0; $k - 3];
                                    body.clone_from_slice(&vbody);
                                    thread::spawn(move || {
                                        check_skolem_head_tail(head1, head2, &body, tail)
                                    })
                                }).collect();
                               subsubhandlers
                        }).collect();
                    let collected: Vec<_> = subhandlers.into_iter().flatten().collect();
                    collected
                }).into_iter().flatten().collect();

                handlers.into_iter().map(|x| x.join().unwrap()).sum()
            }

            let now = Instant::now();
            let permutations = check_all_skolem();
            let elapsed_time = now.elapsed().as_secs_f32();
            println!("k = {:0>2}, permutations = {:0>5}, time = {}", $k, permutations, elapsed_time);
        }
    };
}

#[allow(unused_macros)]
macro_rules! mt_skolem_dual_head {
    ($k:expr) => {
        {
            fn skolem_check_no_alloc_min_shift(head1: u8, head2: u8, ordering: [u8; $k - 2]) -> bool {
                let (mut skolem, mut iters_so_far): (u64, u8) = if head1 == 1 {
                    (1 << (head2 - 1), 3)
                } else {
                    ((1 << (head1 - 2)) | (1 << (head2-1)), 2)
                };

                for &i in &ordering {
                    let x = skolem.trailing_ones() as u8;
                    skolem >>= x;

                    if (skolem & (1 << i)) != 0 {
                        return false;
                    }

                    iters_so_far += x + 1;
                    if iters_so_far > 2 * $k - i {
                        return false;
                    }

                    skolem |= 1 << i;
                    skolem >>= 1;
                }
                true
            }

            fn check_skolem_head_tail(head1: u8, head2: u8, tail: &[u8; $k - 2]) -> usize {
                if head1 - 1 == head2 {
                    return 0;
                }

                let mut x = 0;

                let mut tail = tail.clone();
                let max_valid = ($k * 2 + 2) / 3;

                for tail in permutohedron::Heap::new(&mut tail) {
                    if tail[$k - 3] <= max_valid {
                        if skolem_check_no_alloc_min_shift(head1, head2, tail) {
                            x += 1;
                        }
                    }
                }

                x
            }

            fn check_all_skolem() -> usize {
                if $k == 0 {
                    return 0;
                } else if $k == 1 {
                    return 1;
                } else if [2, 3].contains(&($k % 4)) {
                    return 0;
                }
                let handlers: Vec<_> = (1u8..=$k).into_iter().map(|head1| {
                    let subhandlers: Vec<_> = (1u8..=$k)
                        .filter(|&x| x != head1 && x != head1 - 1)
                        .map(|head2| {
                            let vtail: Vec<u8> = (1u8..=$k).filter(|&j| j != head1 && j != head2).collect();
                            let mut tail = [0; $k - 2];
                            tail.clone_from_slice(&vtail);
                            thread::spawn(move || {
                                check_skolem_head_tail(head1, head2, &tail)
                            })
                        }).collect();
                    subhandlers
                }).into_iter().flatten().collect();

                handlers.into_iter().map(|x| x.join().unwrap()).sum()
            }

            let now = Instant::now();
            let permutations = check_all_skolem();
            let elapsed_time = now.elapsed().as_secs_f32();
            println!("k = {:0>2}, permutations = {:0>5}, time = {}", $k, permutations, elapsed_time);
        }
    };
}

#[allow(unused_macros)]
macro_rules! mt_skolem_head {
    ($k:expr) => {
        {
            fn skolem_check_no_alloc_min_shift(head: u8, ordering: [u8; $k - 1]) -> bool {
                let mut skolem: u32 = 1 << (head - 1);
                let mut iters_so_far = 1;

                for &i in &ordering {
                    let x = skolem.trailing_ones() as u8;
                    skolem >>= x;

                    if (skolem & (1 << i)) != 0 {
                        return false;
                    }

                    iters_so_far += x + 1;
                    if iters_so_far > 2 * $k - i {
                        return false;
                    }

                    skolem |= 1 << i;
                    skolem >>= 1;
                }
                true
            }

            fn check_skolem_head_tail(head: u8, tail: &[u8; $k - 1]) -> usize {
                let mut x = 0;

                let mut tail = tail.clone();
                let max_valid = ($k * 2 + 2) / 3;

                for tail in permutohedron::Heap::new(&mut tail) {
                    if head - 1 != tail[0] && tail[$k - 2] <= max_valid {
                        if skolem_check_no_alloc_min_shift(head, tail) {
                            x += 1;
                        }
                    }
                }

                x
            }

            fn check_all_skolem() -> usize {
                if $k == 0 {
                    return 0;
                } else if $k == 1 {
                    return 1;
                } else if [2, 3].contains(&($k % 4)) {
                    return 0;
                }

                let handlers: Vec<_> = (1u8..=$k).into_iter().map(|v| {
                    let head = v;
                    let mut vtail: Vec<u8> = (1u8..=$k).collect();
                    vtail.remove((v - 1) as usize);
                    let mut tail = [0; $k - 1];
                    tail.clone_from_slice(&vtail);
                    thread::spawn(move || {
                        check_skolem_head_tail(head, &tail)
                    })
                }).collect();

                handlers.into_iter().map(|x| x.join().unwrap()).sum()
            }

            let now = Instant::now();
            let permutations = check_all_skolem();
            let elapsed_time = now.elapsed().as_secs_f32();
            println!("k = {:0>2}, permutations = {:0>5}, time = {}", $k, permutations, elapsed_time);
        }
    };
}

#[allow(unused_macros)]
macro_rules! st_skolem {
    ($k:expr) => {
        {
            use std::fs::File;
            use std::io::{BufWriter, Write};

            fn skolem_check_no_alloc_min_shift(ordering: [u8; $k]) -> bool {
                let mut skolem: u32 = 0;
                let mut iters_so_far = 0;

                // This is basically:
                // Find a1...an such that
                // sum(2^(an)(2^n+1)) = 2^(2*n) - 1
                // sum(2^(an+n)+2^an) = 2^(2*n) - 1
                // sum(2^(an)2^n) + sum(2^an) = 2^(2*n) - 1
                for &i in &ordering {
                    let x = skolem.trailing_ones() as u8;
                    skolem >>= x;

                    if (skolem & (1 << i)) != 0 {
                        return false;
                    }

                    iters_so_far += x + 1;
                    if iters_so_far > 2 * $k - i {
                        return false;
                    }

                    skolem |= 1 << i;
                    skolem >>= 1;
                }
                true
            }

            // fn skolem_check_no_alloc(ordering: [u8; $k]) -> bool {
            //     let mut skolem: u32 = 0;
            //     let mut first = 0u8;
            //     for &i in &ordering {
            //         let mut unbroken = true;
            //         for n in first..2*$k-i {
            //             if (skolem & (1 << n)) != 0 {
            //                 continue;
            //             }
            //             if (skolem & (1 << (n + i))) != 0 {
            //                 return false;
            //             }
            //             first = n + 1;
            //             skolem |= 1 << n;
            //             skolem |= 1 << (n + i);
            //             unbroken = false;
            //             break;
            //         }
            //         if unbroken {
            //             return false;
            //         }
            //     }
            //     true
            // }

            // fn skolem_check(ordering: [u8; $k], skolem: &mut [u8; 2*$k]) -> bool {
            //     skolem.iter_mut().for_each(|x| *x = 0);
            //     let mut first = 0;
            //     for &i in &ordering {
            //         let mut unbroken = true;
            //         for n in first..2*$k-(i as usize) {
            //             if skolem[n] != 0 {
            //                 continue;
            //             }
            //             if skolem[n + (i as usize)] != 0 {
            //                 return false;
            //             }
            //             first = n + 1;
            //             skolem[n] = i;
            //             skolem[n + (i as usize)] = i;
            //             unbroken = false;
            //             break;
            //         }
            //         if unbroken {
            //             return false;
            //         }
            //     }
            //     true
            // }

            fn check_all_skolem() -> usize {
                if $k == 0 {
                    return 0;
                } else if $k == 1 {
                    return 1;
                } else if [2, 3].contains(&($k % 4)) {
                    return 0;
                }

                let mut x = 0;

                let mut p = [0u8; $k];
                p.iter_mut().zip((1u8..=$k).into_iter()).for_each(|(p, v)| *p = v);
                let max_valid = ($k * 2 + 2) / 3;
                for p in permutohedron::Heap::new(&mut p) {
                    if p[0] - 1 != p[1] && p[$k - 1] <= max_valid {
                        if skolem_check_no_alloc_min_shift(p) {
                            x += 1;
                        }
                    }
                }
                x
            }

            fn write_all_skolem_to_file() -> Result<usize, std::io::Error> {
                if $k == 0 {
                    return Ok(0);
                } else if $k == 1 {
                    return Ok(1);
                } else if [2, 3].contains(&($k % 4)) {
                    return Ok(0);
                }

                let mut x = 0;

                let mut p = [0u8; $k];
                p.iter_mut().zip((1u8..=$k).into_iter()).for_each(|(p, v)| *p = v);
                let max_valid = ($k + 3) / 2;
                let mut f = File::create(format!("skolem{}.txt", $k))?;
                let mut f = BufWriter::new(f);
                let max = ($k * 2 + 2) / 3;
                for p in permutohedron::Heap::new(&mut p) {
                    if p[$k - 1] == 1 {
                        continue;
                    }
                    if p[0] - 1 != p[1] && p[$k-1] <= max {
                        if skolem_check_no_alloc_min_shift(p) {
                            f.write_all(format!("{:?}\n", p).as_bytes())?;
                            // println!("{:?},", p);
                            x += if p[0] == 1 {2} else {1};
                        }
                    }
                }
                Ok(x)
            }

            let now = Instant::now();
            let permutations = check_all_skolem();
            let elapsed_time = now.elapsed().as_secs_f32();
            println!("k = {:0>2}, permutations = {:0>5}, time = {}", $k, permutations, elapsed_time);
        }
    };
}

macro_rules! macro_for_each {
    ($x:ident; $($k:expr),+) => {
        $(
            $x!($k);
        )*
    };

}

// fn skolem_gen(ordering: Vec<u8>, skolem: &mut Vec<u8>) -> bool {
//     let len = skolem.len();
//     skolem.iter_mut().for_each(|x| *x = 0);
//     let mut first = 0;
//     for i in ordering {
//         let mut unbroken = true;
//         for n in first..len-(i as usize) {
//             if skolem[n] == 0 {
//                 if skolem[n + (i as usize)] != 0 {
//                     return false;
//                 }
//                 first = n + 1;
//                 skolem[n] = i;
//                 skolem[n + (i as usize)] = i;
//                 unbroken = false;
//                 break;
//             }
//         }
//         if unbroken {
//             return false;
//         }
//     }
//     true
// }
//
// fn factorial(num: usize) -> usize {
//     if num == 0 {
//         1
//     } else {
//         num * factorial(num - 1)
//     }
// }
//
// fn everything(k: usize) -> usize{
//     if k == 0 {
//         return 0;
//     } else if k == 1 {
//         return 1;
//     } else if [2, 3].contains(&(k % 4)) {
//         return 0;
//     }
//
//     let mut x = 0;
//
//     let mut p: Vec<u8> = (1u8..=k as u8).into_iter().collect();
//     let mut skolem = vec![0; 2 * k];
//     for p in permutohedron::Heap::new(&mut p) {
//         if p[0] - 1 != p[1] {
//             if skolem_gen(p, &mut skolem) {
//                 x += 1;
//             }
//         }
//     }
//     x
// }


// Expected
// k = 02, permutations = 00000, time = 0.0000001
// k = 03, permutations = 00000, time = 0.0000005
// k = 04, permutations = 00006, time = 0.0000008
// k = 05, permutations = 00010, time = 0.0000035
// k = 06, permutations = 00000, time = 0
// k = 07, permutations = 00000, time = 0.0000001
// k = 08, permutations = 00504, time = 0.0012897
// k = 09, permutations = 02656, time = 0.0116646
// k = 10, permutations = 00000, time = 0.0000003
// k = 11, permutations = 00000, time = 0.0000001
// k = 12, permutations = 455936, time = 13.0812845
// xx
// k = 02, permutations = 00000, time = 0.0000001
// k = 03, permutations = 00000, time = 0.0000005
// k = 04, permutations = 00006, time = 0.0000008
// k = 05, permutations = 00010, time = 0.0000035
// k = 06, permutations = 00000, time = 0
// k = 07, permutations = 00000, time = 0.0000001
// k = 08, permutations = 00504, time = 0.001122
// k = 09, permutations = 02656, time = 0.0112071
// k = 10, permutations = 00000, time = 0.0000001
// k = 11, permutations = 00000, time = 0.0000002
// k = 12, permutations = 455936, time = 11.5821295
// xx
// k = 02, permutations = 00000, time = 0.0000002
// k = 03, permutations = 00000, time = 0
// k = 04, permutations = 00006, time = 0.0000005
// k = 05, permutations = 00010, time = 0.0000024
// k = 06, permutations = 00000, time = 0.0000001
// k = 07, permutations = 00000, time = 0
// k = 08, permutations = 00504, time = 0.0007367
// k = 09, permutations = 02656, time = 0.0056482
// k = 10, permutations = 00000, time = 0
// k = 11, permutations = 00000, time = 0
// k = 12, permutations = 455936, time = 11.438467
// k = 13, permutations = 3040560, time = 115.34939
// xx
// k = 02, permutations = 00000, time = 0.0000012
// k = 03, permutations = 00000, time = 0
// k = 04, permutations = 00006, time = 0.0000005
// k = 05, permutations = 00010, time = 0.0000025
// k = 06, permutations = 00000, time = 0.0000001
// k = 07, permutations = 00000, time = 0
// k = 08, permutations = 00504, time = 0.0007311
// k = 09, permutations = 02656, time = 0.0050665
// k = 10, permutations = 00000, time = 0.0000001
// k = 11, permutations = 00000, time = 0.0000001
// k = 12, permutations = 455936, time = 7.4603395
// k = 13, permutations = 3040560, time = 96.6979
// xx
// k = 02, permutations = 00000, time = 0.0000002
// k = 03, permutations = 00000, time = 0.0000001
// k = 04, permutations = 00006, time = 0.0003665
// k = 05, permutations = 00010, time = 0.0002327
// k = 06, permutations = 00000, time = 0.0000001
// k = 07, permutations = 00000, time = 0.0000001
// k = 08, permutations = 00504, time = 0.0004112
// k = 09, permutations = 02656, time = 0.0011961
// k = 10, permutations = 00000, time = 0.0000001
// k = 11, permutations = 00000, time = 0.0000001
// k = 12, permutations = 455936, time = 1.5835946
// k = 13, permutations = 3040560, time = 14.678945
// xx
// k = 02, permutations = 00000, time = 0.0000002
// k = 03, permutations = 00000, time = 0.0000001
// k = 04, permutations = 00006, time = 0.0002174
// k = 05, permutations = 00010, time = 0.0002464
// k = 06, permutations = 00000, time = 0.0000002
// k = 07, permutations = 00000, time = 0.0000001
// k = 08, permutations = 00504, time = 0.000405
// k = 09, permutations = 02656, time = 0.0010108
// k = 10, permutations = 00000, time = 0.0000001
// k = 11, permutations = 00000, time = 0.0000002
// k = 12, permutations = 455936, time = 0.85736626
// k = 13, permutations = 3040560, time = 11.101549
fn main() {
    macro_for_each!(mt_skolem_dual_head_tail; 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
    macro_for_each!(mt_skolem_dual_head; 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
    macro_for_each!(mt_skolem_head; 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
    macro_for_each!(st_skolem; 3, 4, 5, 6, 7, 8, 9, 10, 11, 12);

    // skolem_mt_dual_head_for_each!(3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
    // skolem_mt_fn_for_each!(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
    // skolem_fn_for_each!(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);
}